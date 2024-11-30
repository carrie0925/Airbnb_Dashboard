import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import sqlite3

# 資料庫連接與查詢
db_path = "C:/Users/CARRIE/Desktop/NTHU/DDS/4.final_project/Airbnb_Dashboard/data_final.db"  # 替換為您的資料庫路徑
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

# 初始化 Dash 應用
app = dash.Dash(__name__)

app.layout = html.Div([
    # 標題
    html.H1("紐約市房源價格箱型圖", style={
        "text-align": "center",
        "font-family": "Arial, sans-serif",
        "color": "#333",
        "margin-bottom": "20px"
    }),
    
    # Checkbox 用於選擇行政區
    html.Div([
        html.Label("選擇行政區：", style={
            "font-size": "18px",
            "font-weight": "bold",
            "margin-bottom": "10px"
        }),
        dcc.Checklist(
            id="borough-checklist",
            options=[{"label": borough, "value": borough} for borough in df["borough"].unique()],
            value=[],  # 默認不選
            inline=True,  # 水平排列
            style={"font-size": "16px", "margin": "10px"}
        )
    ], style={
        "padding": "20px",
        "background-color": "#f5f5f5",
        "border-radius": "10px",
        "margin-bottom": "20px"
    }),

    # 圖表區域
    dcc.Graph(id="boxplot-graph", style={
        "border": "1px solid #ddd",
        "border-radius": "10px",
        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
    }),
], style={
    "font-family": "Arial, sans-serif",
    "background-color": "#fafafa",
    "padding": "30px"
})


# 回調函數動態更新圖表
@app.callback(
    Output("boxplot-graph", "figure"),
    [Input("borough-checklist", "value")]
)
def update_boxplot(selected_boroughs):
    # 如果未選擇任何行政區，僅基於房源類型繪製圖表
    if not selected_boroughs:
        fig_room = px.box(
            df,
            x="room_type",
            y="price",
            title="不同房源類型每晚價格的箱型圖",
            labels={"room_type": "room type", "price": "price per night"},
            color_discrete_sequence=["#87CEFA"],  # 單色，統一樣式
            hover_data=["listing_id", "host_name"] 
        )
    else:
        # 過濾選定行政區
        filtered_df = df[df["borough"].isin(selected_boroughs)]
        fig_room = px.box(
            filtered_df,
            x="room_type",
            y="price",
            color="borough",
            title="不同行政區每晚價格的箱型圖",
            labels={"room_type": "room type", "price": "price per night"},
            color_discrete_map=custom_colors,  # 使用自定義色票
            hover_data=["listing_id", "host_name"] 
        )
    
    # 圖表美化
    fig_room.update_layout(
        yaxis=dict(
            range=[0, 1000],
            title=dict(text="price per night(US):", font=dict(size=16, color="#333")),
            gridcolor="rgba(200,200,200,0.2)"
        ),
        xaxis=dict(
            title=dict(text="room type:", font=dict(size=16, color="#333")),
            tickfont=dict(size=14, color="#333")
        ),
        title=dict(
            font=dict(size=22, color="#555"),
            x=0.5,  # 標題居中
        ),
        font=dict(size=14, family="Arial, sans-serif"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(t=50, b=50, l=50, r=50),
        legend=dict(
            title="行政區域",
            font=dict(size=14),
            bordercolor="#ddd",
            borderwidth=1
        )
    )
    # 去除虛線，取消箱型圖的 notched 和 boxmean 數據顯示
    fig_room.update_traces(
        marker=dict(line=dict(width=1.5)),
        boxmean=False,  # 不顯示均值或標準差
        hovertemplate=(
        "Host name: %{customdata[0]}<br>"
        "Listing ID: %{customdata[1]}<br>"
        "Price per night (US): %{y}<extra></extra>"
    )

    )

    return fig_room


# 啟動應用
if __name__ == "__main__":
    app.run_server(debug=True)