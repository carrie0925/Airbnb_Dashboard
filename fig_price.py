import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# Dash 應用初始化
app = dash.Dash(__name__)

# 資料庫連接與查詢
db_path = os.getenv("DB_PATH")  # 從環境變數讀取資料庫路徑
conn = sqlite3.connect(db_path)

# 修正 SQL 查詢
query = """
SELECT 
    b.borough_name AS borough,
    round(AVG(l.price), 2) AS AveragePrice,
    COUNT(l.listing_id) AS NumberOfProperties
FROM 
    listings l
JOIN 
    locations loc ON l.listing_id = loc.listing_id
JOIN 
    borough b ON loc.borough_id = b.borough_id  -- 使用正確的欄位名稱
WHERE 
    b.borough_name IN ('Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island')
    AND l.price IS NOT NULL
    AND l.price > 0
GROUP BY 
    b.borough_name;
"""
df = pd.read_sql_query(query, conn)

# 關閉資料庫連接
conn.close()

# 自定義行政區域顏色
borough_colors = {
    "Manhattan": "#ff928b",
    "Brooklyn": "#ffac81",
    "Queens": "#fec3a6",
    "Bronx": "#efe9ae",
    "Staten Island": "#cdeac0"
}

# 構造圖表
fig = go.Figure()

# 長條圖：房源數量（左側 Y 軸）
fig.add_trace(go.Bar(
    x=df['borough'],  # X 軸：行政區名稱
    y=df['NumberOfProperties'],  # Y 軸：房源數量
    marker_color=[borough_colors[borough] for borough in df['borough']],  # 對應行政區顏色
    name='Number of Properties',
    yaxis='y'  # 將此圖表綁定到左側 Y 軸
))

# 折線圖：平均價格（右側 Y 軸）
fig.add_trace(go.Scatter(
    x=df['borough'],  # X 軸：行政區名稱
    y=df['AveragePrice'],  # Y 軸：平均價格
    mode='lines+markers',  # 折線加數據點
    line=dict(color='#333333', width=2),  # 折線顏色設定為灰黑色
    marker=dict(color='#000000', size=10),  # 數據點顏色設定為黑色
    name='Average Price ($)',
    yaxis='y2'  # 將此圖表綁定到右側 Y 軸
))

# 更新圖表格式，啟用雙 Y 軸
fig.update_layout(
    title="Average Price and Number of Properties by Borough",
    xaxis_title="Boroughs",
    yaxis=dict(
        title="Number of Properties",  # 左側 Y 軸標題
        titlefont=dict(color="#333333"),  # 左側 Y 軸顏色
        tickfont=dict(color="#333333")   # 左側刻度文字顏色
    ),
    yaxis2=dict(
        title="Average Price ($)",  # 右側 Y 軸標題
        titlefont=dict(color="#333333"),  # 右側 Y 軸顏色
        tickfont=dict(color="#333333"),  # 右側刻度文字顏色
        overlaying="y",  # 將右側 Y 軸與左側 Y 軸重疊
        side="right"  # 右側顯示
    ),
    legend=dict(
        title="Metrics"
    ),
    template="plotly_white"
)

# Dash 應用佈局
app.layout = html.Div([
    html.H1("Bar and Line Chart with Dual Y-Axis", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)  # 直接呈現圖表
])

# 啟動應用
if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# Dash 應用初始化
app = dash.Dash(__name__)

# 資料庫連接與查詢
db_path = os.getenv("DB_PATH")  # 從環境變數讀取資料庫路徑
conn = sqlite3.connect(db_path)

# 修正 SQL 查詢
query = """
SELECT 
    b.borough_name AS borough,
    round(AVG(l.price), 2) AS AveragePrice,
    COUNT(l.listing_id) AS NumberOfProperties
FROM 
    listings l
JOIN 
    locations loc ON l.listing_id = loc.listing_id
JOIN 
    borough b ON loc.borough_id = b.borough_id  -- 使用正確的欄位名稱
WHERE 
    b.borough_name IN ('Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island')
    AND l.price IS NOT NULL
    AND l.price > 0
GROUP BY 
    b.borough_name;
"""
df = pd.read_sql_query(query, conn)

# 關閉資料庫連接
conn.close()

# 自定義行政區域顏色
borough_colors = {
    "Manhattan": "#ff928b",
    "Brooklyn": "#ffac81",
    "Queens": "#fec3a6",
    "Bronx": "#efe9ae",
    "Staten Island": "#cdeac0"
}

# 構造圖表
fig = go.Figure()

# 長條圖：房源數量（左側 Y 軸）
fig.add_trace(go.Bar(
    x=df['borough'],  # X 軸：行政區名稱
    y=df['NumberOfProperties'],  # Y 軸：房源數量
    marker_color=[borough_colors[borough] for borough in df['borough']],  # 對應行政區顏色
    name='Number of Properties',
    yaxis='y'  # 將此圖表綁定到左側 Y 軸
))

# 折線圖：平均價格（右側 Y 軸）
fig.add_trace(go.Scatter(
    x=df['borough'],  # X 軸：行政區名稱
    y=df['AveragePrice'],  # Y 軸：平均價格
    mode='lines+markers',  # 折線加數據點
    line=dict(color='#333333', width=2),  # 折線顏色設定為灰黑色
    marker=dict(color='#000000', size=4),  # 數據點顏色設定為黑色
    name='Average Price ($)',
    yaxis='y2'  # 將此圖表綁定到右側 Y 軸
))

# 更新圖表格式，啟用雙 Y 軸
fig.update_layout(
    title="Average Price and Number of Properties by Borough",
    xaxis_title="Boroughs",
    yaxis=dict(
        title="Number of Properties",  # 左側 Y 軸標題
        titlefont=dict(color="#333333"),  # 左側 Y 軸顏色
        tickfont=dict(color="#333333")   # 左側刻度文字顏色
    ),
    yaxis2=dict(
        title="Average Price ($)",  # 右側 Y 軸標題
        titlefont=dict(color="#333333"),  # 右側 Y 軸顏色
        tickfont=dict(color="#333333"),  # 右側刻度文字顏色
        overlaying="y",  # 將右側 Y 軸與左側 Y 軸重疊
        side="right"  # 右側顯示
    ),
    legend=dict(
        title="Metrics"
    ),
    template="plotly_white"
)

# Dash 應用佈局
app.layout = html.Div([
    html.H1("Bar and Line Chart with Dual Y-Axis", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)  # 直接呈現圖表
])

# 啟動應用
if __name__ == '__main__':
    app.run_server(debug=True)
