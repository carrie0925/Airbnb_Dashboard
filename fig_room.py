import dash
from dash import dcc, html
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
            "Manhattan": "#f9a980",
            "Brooklyn": "#ede46a",
            "Queens": "#b6c17d",
            "Bronx": "#e3b054",
            "Staten Island": "#e3b054"
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

        # 圖表美化
        fig.update_layout(
            showlegend=False,  # 禁用圖例
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
            margin=dict(t=50, b=50, l=50, r=50)
        )

        # 更新 trace 設定
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

if __name__ == "__main__":
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H2("Room Type Analysis", 
                style={'text-align': 'center'}),
        dcc.Graph(figure=create_room_figure())
    ])
    app.run_server(debug=True)