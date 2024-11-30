import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 資料庫連接與查詢
db_path = os.getenv("DB_PATH")  # 替換為您的資料庫路徑
conn = sqlite3.connect(db_path)

query = """
SELECT 
    b.borough_name AS borough,
    b.tourist_revenue AS tourist_revenue,
    SUM(s.crime_level_weight) AS crime_score
FROM 
    borough b
LEFT JOIN 
    security s ON b.borough_id = s.borough_id
GROUP BY 
    b.borough_id, b.borough_name, b.tourist_revenue;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 計算平均值
avg_crime_score = df["crime_score"].mean()
avg_tourism_revenue = df["tourist_revenue"].mean()

# 繪製圖表
fig = go.Figure()

# Crime Score
fig.add_trace(go.Scatter(
    x=df["borough"],
    y=df["crime_score"],
    mode="lines+markers",
    name="Crime Score",
    line=dict(color="#89cff0", width=2),  # 藍色
    marker=dict(size=8),
    hovertemplate="Crime Score: %{y}<br>Borough: %{x}<extra></extra>",
    yaxis="y1"  # 綁定左側 y 軸
))

# Tourism Revenue
fig.add_trace(go.Scatter(
    x=df["borough"],
    y=df["tourist_revenue"],
    mode="lines+markers",
    name="Tourism Revenue",
    line=dict(color="#ff928b", width=2),  # 紅色
    marker=dict(size=8),
    hovertemplate="Tourism Revenue: %{y}<br>Borough: %{x}<extra></extra>",
    yaxis="y2"  # 綁定右側 y 軸
))

# 平均 Crime Score (虛線)
fig.add_trace(go.Scatter(
    x=df["borough"],
    y=[avg_crime_score] * len(df),
    mode="lines",
    name="Avg Crime Score",
    line=dict(color="#89cff0", dash="dash", width=1.5),
    hovertemplate="Avg Crime Score: %{y}<extra></extra>",  # 移除 <extra></extra> 外部的多余信息
    yaxis="y1",  # 綁定左側 y 軸
    showlegend=True
))

# 平均 Tourism Revenue (虛線)
fig.add_trace(go.Scatter(
    x=df["borough"],
    y=[avg_tourism_revenue] * len(df),
    mode="lines",
    name="Avg Tourism Revenue",
    line=dict(color="#ff928b", dash="dash", width=1.5),
    hovertemplate="Avg Tourism Revenue: %{y}<extra></extra>",  # 移除 <extra></extra> 外部的多余信息
    yaxis="y2",  # 綁定右側 y 軸
    showlegend=True
))

# 更新佈局
fig.update_layout(
    xaxis=dict(title="Borough"),
    yaxis=dict(
        title="Crime Score",
        side="left",
        showgrid=True,  # 左側網格線
        gridcolor="lightgray",  # 統一的網格線顏色
    ),
    yaxis2=dict(
        title="Tourism Revenue",
        overlaying="y",  # 疊加在 y 軸上
        side="right",
        showgrid=False  # 關閉右側網格線
    ),
    legend=dict(
        orientation="h",  # 水平排列
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    template="plotly_white"
)

# 初始化 Dash 應用
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("New York City Tourism Revenue and Safety Score Comparison"),
    dcc.Graph(figure=fig),  # 直接將圖表傳遞給 Graph
])

if __name__ == "__main__":
    app.run_server(debug=True)