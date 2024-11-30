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
        "Bronx": (185,55),
        "Brooklyn": (140, 185),
        "Manhattan": (120, 110),
        "Queens": (230, 140),
        "Staten Island": (55, 220)
    }

    # 建立 Plotly 地圖
    fig_map = go.Figure()

    # 設定圖片作為背景
    fig_map.update_layout(
        images=[
            dict(
                source=img,
                x=0, y=0, xref="x", yref="y",
                sizex=320, sizey=256,  # 圖片尺寸
                xanchor="left", yanchor="bottom",
                layer="below"
            )
        ],
        xaxis=dict(range=[0, 320], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 256], showgrid=False, zeroline=False, visible=False),
        showlegend=False,
        template="plotly_white",
        width=320,
        height=256,
        margin=dict(l=0, r=0, t=0, b=0)  # 移除邊距
    )

    # 添加行政區互動點
    for borough, pos in positions.items():
        if borough in data_dict:  # 確保 borough 名稱在 SQL 查詢結果中
            listings_count = data_dict[borough]["listings_count"]
            tourism_value = data_dict[borough]["tourism_value"]
            hover_text = (
                f"<b style='font-size:10px;'>{borough}</b><br>"
                f"Total Listing Count: {listings_count}<br>"
                f"Expected Tourism Value: ${tourism_value} millions"
            )
            fig_map.add_trace(
                go.Scatter(
                    x=[pos[0]],
                    y=[256 - pos[1]],
                    mode="markers",
                    marker=dict(
                        size=6, 
                        color="Beige",
                        line=dict(color="black", width=1)
                    ),
                    hoverinfo="none",
                    hovertext=hover_text,
                    hoverlabel=dict(
                        font=dict(size=12),
                        bgcolor="white",
                        bordercolor="black",
                    ),
                    customdata=[[
                        borough,
                        listings_count,
                        tourism_value
                    ]],
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
            config={"scrollZoom": False},
            style={"width": "1000px", "height": "800px", "margin": "auto"}
        )
    ])
    app.run_server(debug=True)