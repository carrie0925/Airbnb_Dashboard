import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import sqlite3
from dotenv import load_dotenv
import os

def create_map_figure():
    """創建地圖圖表的函數"""
    # read env path
    dotenv_path = os.getenv("DOTENV_PATH")
    load_dotenv(dotenv_path=dotenv_path)
    db_path = os.getenv("DB_PATH")
    image_path = os.getenv("IMAGE_PATH")

    img = Image.open(image_path)
    conn = sqlite3.connect(db_path)

    # 查詢行政區房源數和觀光價值
    query = """
    SELECT 
        b.borough_name AS borough, 
        COUNT(l.listing_id) AS listings_count,
        b.tourist_revenue AS tourism_value
    FROM 
        borough b
    JOIN 
        locations loc ON b.borough_id = loc.borough_id
    JOIN 
        listings l ON loc.listing_id = l.listing_id
    GROUP BY 
        b.borough_id, b.borough_name;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 提取資料，轉換為字典結構
    data_dict = df.set_index("borough").to_dict(orient="index")

    # 五大行政區的位置（基於圖片像素座標）
    positions = {
        "Bronx": (290, 86),
        "Brooklyn": (230, 290),
        "Manhattan": (188, 172),
        "Queens": (360, 200),
        "Staten Island": (100, 344)
    }

    # 建立 Plotly 地圖
    fig_map = go.Figure()

    # 設定圖片作為背景
    fig_map.update_layout(
        images=[
            dict(
                source=img,
                x=0, y=0, xref="x", yref="y",
                sizex=500, sizey=400,  # 圖片尺寸
                xanchor="left", yanchor="bottom",
                layer="below"
            )
        ],
        xaxis=dict(
            range=[0, 500], 
            showgrid=False, 
            zeroline=False, 
            visible=False,
            scaleanchor="y",
            constrain="domain"
        ),
        yaxis=dict(
            range=[0, 400], 
            showgrid=False, 
            zeroline=False, 
            visible=False,
            constrain="domain"
        ),
        showlegend=False,
        template="plotly_white",
        width=500,   # 整體寬度
        height=400,  # 整體高度
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # 添加行政區互動點
    for borough, pos in positions.items():
        if borough in data_dict:
            listings_count = data_dict[borough]["listings_count"]
            tourism_value = data_dict[borough]["tourism_value"]
            
            hover_text = (
                f"<b>{borough}</b><br>"
                f"Total Listing Count: {listings_count:,}<br>"
                f"Expected Tourism Value: ${tourism_value:,}M"
            )
            
            fig_map.add_trace(
                go.Scatter(
                    x=[pos[0]],
                    y=[400 - pos[1]],  # 反轉 y 座標
                    mode="markers",
                    marker=dict(
                        size=12,
                        color="darkred",
                        symbol="circle",
                    ),
                    hoverinfo="text",
                    hovertext=hover_text,
                    hoverlabel=dict(
                        bgcolor="white",
                        bordercolor="black",
                        font=dict(size=12)
                    ),
                    customdata=[[borough, listings_count, tourism_value]],
                    name=borough
                )
            )

    fig_map.update_layout(
        hoverdistance=5,
        hovermode='closest',
        clickmode='event'
    )
    
    return fig_map
    """創建地圖圖表的函數"""
    # read env path
    dotenv_path = os.getenv("DOTENV_PATH")
    load_dotenv(dotenv_path=dotenv_path)
    db_path = os.getenv("DB_PATH")
    image_path = os.getenv("IMAGE_PATH")

    img = Image.open(image_path)
    conn = sqlite3.connect(db_path)

    # 查詢行政區房源數和觀光價值
    query = """
    SELECT 
        b.borough_name AS borough, 
        COUNT(l.listing_id) AS listings_count,
        b.tourist_revenue AS tourism_value
    FROM 
        borough b
    JOIN 
        locations loc ON b.borough_id = loc.borough_id
    JOIN 
        listings l ON loc.listing_id = l.listing_id
    GROUP BY 
        b.borough_id, b.borough_name;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 提取資料，轉換為字典結構
    data_dict = df.set_index("borough").to_dict(orient="index")

    # 五大行政區的位置（基於圖片像素座標）
    positions = {
        "Bronx": (290, 60),
        "Brooklyn": (240, 280),
        "Manhattan": (200, 165),
        "Queens": (370, 200),
        "Staten Island": (86, 344)
    }

    # 建立 Plotly 地圖
    fig_map = go.Figure()

    # 設定圖片作為背景
    fig_map.update_layout(
        images=[
            dict(
                source=img,
                x=0, y=0, xref="x", yref="y",
                sizex=550, sizey=440,  # 圖片尺寸
                xanchor="left", yanchor="bottom",
                layer="below"
            )
        ],
        xaxis=dict(range=[0, 550], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 440], showgrid=False, zeroline=False, visible=False),
        showlegend=False,
        template="plotly_white",
        width=550,  # 增加寬度
        height=440,  # 增加高度
        margin=dict(l=0, r=0, t=0, b=0)  # 移除邊距
    )


    # 添加行政區互動點
    for borough, pos in positions.items():
        if borough in data_dict:  # 確保 borough 名稱在 SQL 查詢結果中
            listings_count = data_dict[borough]["listings_count"]
            tourism_value = data_dict[borough]["tourism_value"]

            hover_text = (
                f"<b>{borough}</b><br>"
                f"Total Listing Count: {listings_count:,}<br>"
                f"Expected Tourism Value: ${tourism_value:,}M"
            )
            
            # 添加圓形標記點
            fig_map.add_trace(
                go.Scatter(
                    x=[pos[0]],
                    y=[400 - pos[1]],  # 轉換 y 座標
                    mode="markers",
                    marker=dict(
                        size=12,
                        color="darkred",
                        symbol="circle",
                    ),
                    hoverinfo="text",
                    hovertext=hover_text,
                    hoverlabel=dict(
                        bgcolor="white",
                        bordercolor="black",
                        font=dict(size=12)
                    ),
                    customdata=[[borough, listings_count, tourism_value]],
                    name=borough
                )
            )

    fig_map.update_layout(
        hoverdistance=5,  # 減少hover觸發距離
        hovermode='closest',  # 確保只顯示最近的點的資訊
        clickmode='event'  # 啟用點擊事件
    )
    
    return fig_map

# 如果直接運行此文件，則啟動獨立的 Dash 應用
if __name__ == "__main__":
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("紐約市五大行政區互動地圖", style={"text-align": "center"}),
        dcc.Graph(
            id="interactive-map",
            figure=create_map_figure(),
            config={"displayModeBar": False},
            style={"width": "400px", "height": "320px", "margin": "auto"}
        )
    ])
    app.run_server(debug=True)