import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import sqlite3
from dotenv import load_dotenv
import os

def create_room_figure(selected_boroughs=None):
    """創建房型分析箱型圖"""
    try:
        # 載入環境變數
        load_dotenv()
        
        # 資料庫連接與查詢
        db_path = os.getenv("DB_PATH")
        if not db_path:
            raise ValueError("DB_PATH environment variable not found")
            
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            b.borough_name AS borough,
            l.listing_id AS listing_id,
            h.host_name AS host_name,
            l.room_type AS room_type,
            l.price AS price
        FROM 
            listings l
        JOIN 
            locations loc ON l.listing_id = loc.listing_id
        JOIN 
            borough b ON loc.borough_id = b.borough_id
        JOIN
            hosts h ON l.host_id = h.host_id;
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()

        # 過濾房源類型
        room_types = ["Private room", "Entire home/apt", "Hotel room", "Shared room"]
        df = df[df["room_type"].isin(room_types)]

        # 自定義色票
        custom_colors = {
            "Manhattan": "#ff928b",
            "Brooklyn": "#ffac81",
            "Queens": "#fec3a6",
            "Bronx": "#efe9ae",
            "Staten Island": "#cdeac0"
        }

        # 根據選擇的行政區過濾數據
        if selected_boroughs and len(selected_boroughs) > 0:
            df = df[df["borough"].isin(selected_boroughs)]
            fig = px.box(
                df,
                x="room_type",
                y="price",
                color="borough",
                title="Price Distribution by Room Type and Borough",
                labels={"room_type": "Room Type", "price": "Price per Night ($)"},
                color_discrete_map=custom_colors,
                hover_data=["listing_id", "host_name"]
            )
        else:
            fig = px.box(
                df,
                x="room_type",
                y="price",
                title="Price Distribution by Room Type",
                labels={"room_type": "Room Type", "price": "Price per Night ($)"},
                color_discrete_sequence=["#87CEFA"],
                hover_data=["listing_id", "host_name"]
            )

        # 圖表美化
        fig.update_layout(
            yaxis=dict(
                range=[0, 1000],
                title=dict(text="Price per Night ($)", font=dict(size=14)),
                gridcolor="rgba(200,200,200,0.2)",
                tickfont=dict(size=12)
            ),
            xaxis=dict(
                title=dict(text="Room Type", font=dict(size=14)),
                tickfont=dict(size=12)
            ),
            title=dict(
                font=dict(size=20),
                x=0.5
            ),
            font=dict(family="Arial, sans-serif"),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            legend=dict(
                title="Borough",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        fig.update_traces(
            marker=dict(line=dict(width=1.5)),
            boxmean=False,
            hovertemplate=(
                "Host Name: %{customdata[1]}<br>" +
                "Listing ID: %{customdata[0]}<br>" +
                "Price per Night: $%{y:,.2f}<extra></extra>"
            )
        )

        return fig
    
    except Exception as e:
        print(f"Error creating room figure: {e}")
        fig = px.box(
            pd.DataFrame({'x': [], 'y': []}),
            title="Error Loading Room Data"
        )
        fig.add_annotation(
            text="Error loading room data. Please check database connection.",
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=14)
        )
        return fig

def create_room_layout():
    """創建房型分析頁面布局"""
    try:
        load_dotenv()
        conn = sqlite3.connect(os.getenv("DB_PATH"))
        df = pd.read_sql_query("SELECT DISTINCT borough_name FROM borough", conn)
        conn.close()
        
        return html.Div([
            html.H2("Room Type Analysis", 
                    style={'text-align': 'center', 'margin-bottom': '20px'}),
            
            html.Div([
                html.Label("Select Boroughs:", style={
                    'font-size': '16px',
                    'font-weight': 'bold',
                    'margin-bottom': '10px'
                }),
                dcc.Checklist(
                    id="borough-checklist",
                    options=[{"label": borough, "value": borough} 
                            for borough in df['borough_name']],
                    value=[],
                    inline=True,
                    style={'font-size': '14px', 'margin': '10px'}
                )
            ], style={
                'padding': '20px',
                'background-color': '#f5f5f5',
                'border-radius': '10px',
                'margin-bottom': '20px'
            }),
            
            dcc.Graph(
                id="boxplot-graph",
                figure=create_room_figure(),
                style={
                    'border': '1px solid #ddd',
                    'border-radius': '10px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }
            )
        ], style={
            'padding': '20px',
            'background-color': '#fafafa'
        })
    
    except Exception as e:
        print(f"Error creating layout: {e}")
        return html.Div("Error loading layout. Please check database connection.")

# 如果直接運行此文件，則啟動獨立的 Dash 應用
if __name__ == "__main__":
    app = dash.Dash(__name__)
    
    app.layout = create_room_layout()
    
    @app.callback(
        Output("boxplot-graph", "figure"),
        [Input("borough-checklist", "value")]
    )
    def update_boxplot(selected_boroughs):
        return create_room_figure(selected_boroughs)
    
    app.run_server(debug=True)