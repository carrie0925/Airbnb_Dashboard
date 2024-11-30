import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import sqlite3
import os

os.chdir("C:/Users/CARRIE/Desktop/NTHU/DDS/4.final_project/Airbnb_Dashboard")

# 加載圖片
img = Image.open("map_final.jpg")

# 資料庫連接與查詢
db_path = "C:/Users/CARRIE/Desktop/NTHU/DDS/4.final_project/Airbnb_Dashboard/data_final.db"  # 替換為您的資料庫路徑
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
    "Bronx": (500, 170),
    "Brooklyn": (400, 580),
    "Manhattan": (360, 320),
    "Queens": (600, 410),
    "Staten Island": (230, 600),
}

# Dash 應用初始化
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("紐約市五大行政區互動地圖", style={"text-align": "center"}),
    dcc.Graph(
        id="interactive-map",
        config={"scrollZoom": False},  # 禁止滾輪縮放
        style={"width": "1000px", "height": "800px", "margin": "auto"}
    )
])


@app.callback(
    Output("interactive-map", "figure"),
    Input("interactive-map", "id")
)
def update_map(_):
    # 建立 Plotly 地圖
    fig_map = go.Figure()

    # 設定圖片作為背景
    fig_map.update_layout(
        images=[
            dict(
                source=img,
                x=0, y=0, xref="x", yref="y",
                sizex=1000, sizey=800,  # 圖片尺寸
                xanchor="left", yanchor="bottom",
                layer="below"
            )
        ],
        xaxis=dict(range=[0, 1000], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 800], showgrid=False, zeroline=False, visible=False),
        showlegend=False,
        template="plotly_white",
        width=1000,
        height=800,
    )

    # 添加行政區互動點
    for borough, pos in positions.items():
        if borough in data_dict:  # 確保 borough 名稱在 SQL 查詢結果中
            listings_count = data_dict[borough]["listings_count"]
            tourism_value = data_dict[borough]["tourism_value"]
            hover_text = (
                f"<b style='font-size:20px;'>{borough}</b><br>"
                f"Total Listing Count: {listings_count}<br>"
                f"Expected Tourism Value: ${tourism_value} millions"
            )
            fig_map.add_trace(
                go.Scatter(
                    x=[pos[0]],
                    y=[800 - pos[1]],  # Y 軸翻轉以匹配圖片像素座標
                    mode="markers",
                    marker=dict(size=15, color="Beige"),
                    hoverinfo="text",
                    hovertext=hover_text,
                    hoverlabel=dict(
                        font=dict(size=20, color="black"),  # 放大字體，設定文字顏色
                        bgcolor="white",  # 背景色
                    )
                )
            )
    return fig_map


# 啟動應用
if __name__ == "__main__":
    app.run_server(debug=True)

