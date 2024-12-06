import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import sqlite3
from dotenv import load_dotenv
import os

def create_room_figure(selected_boroughs=None, y_range=None):
    """創建房型分析箱型圖"""
    try:
        # 載入環境變數
        load_dotenv()
        
        # 資料庫連接與查詢
        db_path = os.getenv("DB_PATH")
        if not db_path:
            raise ValueError("DB_PATH environment variable not found")
            
        conn = sqlite3.connect(db_path)
        
        # Base query
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
            hosts h ON l.host_id = h.host_id
        WHERE 1=1
        """
        
        # Add borough filtering if selections exist
        if selected_boroughs and len(selected_boroughs) > 0:
            borough_list = "', '".join(selected_boroughs)
            query += f" AND b.borough_name IN ('{borough_list}')"
            
        df = pd.read_sql_query(query, conn)
        conn.close()

        # 過濾房源類型
        room_types = ["Private room", "Entire home/apt", "Hotel room", "Shared room"]
        df = df[df["room_type"].isin(room_types)]

        # 自定義色票
        custom_colors = {
            "Manhattan": "#ff928b",
            "Brooklyn": "#efe9ae",
            "Queens": "#cdeac0",
            "Bronx": "#ffac81",
            "Staten Island": "#fec3a6"
        }

        # 創建圖表
        if selected_boroughs and len(selected_boroughs) > 0:
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
                color_discrete_sequence=["#9c9c7c"],
                hover_data=["listing_id", "host_name"]
            )

        # 設定 y 軸範圍（使用傳入的範圍或默認值）
        y_axis_range = y_range if y_range is not None else [0, 1000]

        # 圖表美化
        fig.update_layout(
            showlegend=False,
            yaxis=dict(
                range=y_axis_range,  # 使用設定的範圍
                title=dict(text="Price per Night ($)", font=dict(size=14)),
                gridcolor="rgba(150, 150, 150, 0.35)",
                tickfont=dict(size=12)
            ),
            xaxis=dict(
                title=dict(text=""),
                tickfont=dict(size=12)
            ),
            title=dict(
                font=dict(size=18),
                x=0.5
            ),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            height=450,
            margin=dict(t=50, b=50, l=50, r=50)
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

# 獨立運行時的測試版面配置
if __name__ == "__main__":
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H2("Room Type Analysis", 
                style={'text-align': 'center', 'margin-bottom': '20px'}),
        
        # 行政區選擇
        html.Div([
            html.Label("Select Boroughs:", style={
                'font-size': '16px',
                'font-weight': 'bold',
                'margin-bottom': '10px',
                'color': 'gray'
            }),
            dcc.Checklist(
                id="borough-checklist",
                options=[
                    {"label": "Manhattan", "value": "Manhattan"},
                    {"label": "Brooklyn", "value": "Brooklyn"},
                    {"label": "Queens", "value": "Queens"},
                    {"label": "Bronx", "value": "Bronx"},
                    {"label": "Staten Island", "value": "Staten Island"}
                ],
                value=[],
                inline=True,
                style={'font-size': '14px', 'margin': '10px'}
            )
        ], style={
            'padding': '20px',
            'background-color': 'white',
            'border-radius': '10px',
            'margin-bottom': '20px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }),

        # 價格範圍選擇
        html.Div([
            html.Label("Select Price Range:", style={
                'font-size': '16px',
                'font-weight': 'bold',
                'margin-bottom': '10px',
                'color': 'gray'
            }),
            dcc.RangeSlider(
                id='price-range-slider',
                min=600,
                max=2000,
                step=None,
                marks={
                    600: '$600',
                    800: '$800',
                    1200: '$1,200',
                    1600: '$1,600',
                    2000: '$2,000'
                },
                value=[600, 2000]
            )
        ], style={
            'padding': '20px',
            'background-color': 'white',
            'border-radius': '10px',
            'margin-bottom': '20px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }),
        
        dcc.Graph(
            id="boxplot-graph",
            figure=create_room_figure(),
            style={
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'background-color': 'white'
            }
        )
    ], style={
        'padding': '20px',
        'background-color': '#f5f5f5'
    })
    
    @app.callback(
        Output("boxplot-graph", "figure"),
        [Input("borough-checklist", "value"),
         Input("price-range-slider", "value")]
    )
    def update_boxplot(selected_boroughs, price_range):
        return create_room_figure(
            selected_boroughs=selected_boroughs,
            y_range=price_range
        )
    
    app.run_server(debug=True)