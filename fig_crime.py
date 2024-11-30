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
db_path = os.getenv("DB_PATH") # 替換為您的資料庫路徑
conn = sqlite3.connect(db_path)

query = """
SELECT 
    b.borough_name AS borough,
    s.crime_level AS crime_type,
    COUNT(s.Event_id) AS crime_count
FROM 
    borough b
LEFT JOIN 
    security s ON b.borough_id = s.borough_id
GROUP BY 
    b.borough_id, b.borough_name, s.crime_level;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 確保資料框內有資料
if df.empty:
    raise ValueError("資料庫查詢結果為空，請檢查數據表結構與內容。")

# 轉換資料以適應堆疊長條圖
pivot_df = df.pivot(index="borough", columns="crime_type", values="crime_count").fillna(0)

# 定義自訂顏色
custom_colors = {
    "VIOLATION": "#6dd3ce",
    "MISDEMEANOR": "#89cff0",
    "FELONY": "#ff928b"
}

# 繪製堆疊長條圖
fig = go.Figure()

for crime_type in pivot_df.columns:
    fig.add_trace(go.Bar(
        x=pivot_df.index,
        y=pivot_df[crime_type],
        name=crime_type,
        marker=dict(color=custom_colors[crime_type]),  # 使用自訂顏色
        hovertemplate="Count: %{y}<br><extra></extra>",
    ))

# 更新佈局
fig.update_layout(
    barmode="stack",  # 堆疊長條圖模式
    xaxis=dict(title="Borough"),
    yaxis=dict(
        title="Crime Count",
        tickvals=[0, 20000, 40000, 60000, 80000, 100000, 120000],  # 明確設定刻度
        tickformat="",  # 顯示完整數值
    ),
    legend=dict(
        title="Crime Type",
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
    html.H2("Distribution of crime types in New York City"),
    dcc.Graph(figure=fig),  # 直接將圖表傳遞給 Graph
])

if __name__ == "__main__":
    app.run_server(debug=True)