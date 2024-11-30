import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

def create_potential_figure():
    """創建觀光收入和安全評分比較圖表"""
    # 載入環境變數
    load_dotenv()
    
    # 資料庫連接與查詢
    db_path = os.getenv("DB_PATH")
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

    # 創建圖表
    fig = go.Figure()

    # Crime Score
    fig.add_trace(go.Scatter(
        x=df["borough"],
        y=df["crime_score"],
        mode="lines+markers",
        name="Crime Score",
        line=dict(color="#cc987c", width=2),
        marker=dict(size=8),
        hovertemplate="Crime Score: %{y}<br>Borough: %{x}<extra></extra>",
        yaxis="y1"
    ))

    # Tourism Revenue
    fig.add_trace(go.Scatter(
        x=df["borough"],
        y=df["tourist_revenue"],
        mode="lines+markers",
        name="Tourism Revenue",
        line=dict(color="#8c7c54", width=2),
        marker=dict(size=8),
        hovertemplate="Tourism Revenue: %{y}<br>Borough: %{x}<extra></extra>",
        yaxis="y2"
    ))

    # 平均 Crime Score (虛線)
    fig.add_trace(go.Scatter(
        x=df["borough"],
        y=[avg_crime_score] * len(df),
        mode="lines",
        name="Avg Crime Score",
        line=dict(color="#cc987c", dash="dash", width=1.5),
        hovertemplate="Avg Crime Score: %{y}<extra></extra>",
        yaxis="y1",
        showlegend=True
    ))

    # 平均 Tourism Revenue (虛線)
    fig.add_trace(go.Scatter(
        x=df["borough"],
        y=[avg_tourism_revenue] * len(df),
        mode="lines",
        name="Avg Tourism Revenue",
        line=dict(color="#8c7c54", dash="dash", width=1.5),
        hovertemplate="Avg Tourism Revenue: %{y}<extra></extra>",
        yaxis="y2",
        showlegend=True
    ))

    # 更新佈局
    fig.update_layout(
        title=dict(
        text="NYC Tourism Revenue vs. Crime Score",
        font=dict(size=15),
        x=0.5,  # 置中標題
        y=0.97  # 稍微往下調整
    ),
        xaxis=dict(
            title="Borough",
            showgrid=True,
            gridcolor="lightgray"
        ),
        yaxis=dict(
            title="Crime Score",
            side="left",
            showgrid=True,
            gridcolor="lightgray",
        ),
        yaxis2=dict(
            title="Tourism Revenue",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11),  # 字體大小
            tracegroupgap=50
        ),
        template="plotly_white",
        height=400,  # 設定固定高度
        margin=dict(l=50, r=50, t=80, b=50)  # 調整邊距
    )

    return fig

# 如果直接運行此文件，則啟動獨立的 Dash 應用
if __name__ == "__main__":
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H2("NYC Tourism Revenue vs. Crime Score",
                style={'text-align': 'left'}),
        dcc.Graph(figure=create_potential_figure())
    ])
    
    app.run_server(debug=True)