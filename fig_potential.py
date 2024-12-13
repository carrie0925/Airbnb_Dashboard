import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import os

def create_potential_figure():
    """創建觀光收入和安全評分比較圖表"""
    try:
        # 使用相對路徑找到資料庫
        def get_db_path():
            """獲取數據庫路徑"""
            if os.environ.get('ENV') == 'production':
                # Heroku 環境
                return os.path.join(os.getcwd(), 'db_final.db')
            else:
                # 本地開發環境
                current_dir = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(current_dir, 'db_final.db')
                db_path = os.path.join(current_dir, "db_final.db")
            
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        
        # SQL查詢，結合 borough 和 security 表格
        query = """
        SELECT 
            b.borough_name,
            b.tourist_revenue,
            SUM(s.crime_level_weight) as crime_score
        FROM 
            borough b
        LEFT JOIN 
            security s ON b.borough_id = s.borough_id
        GROUP BY 
            b.borough_id, b.borough_name, b.tourist_revenue
        ORDER BY 
            b.borough_name;
        """
        
        # 讀取資料
        df = pd.read_sql_query(query, conn)
        conn.close()
        
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
        # 如果讀取失敗，使用備用資料
        df = pd.DataFrame({
            'borough_name': ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'],
            'tourist_revenue': [32831, 2973, 9938, 955, 456],
            'crime_score': [4, 1, 3, 2, 5]
        })

    # 計算平均值
    avg_crime_score = df["crime_score"].mean()
    avg_tourist_revenue = df["tourist_revenue"].mean()

    # 創建圖表
    fig = go.Figure()

    # Crime Score 線圖
    fig.add_trace(go.Scatter(
        x=df["borough_name"],
        y=df["crime_score"],
        mode="lines+markers",
        name="Crime Score",
        line=dict(color="#8C4A2F", width=2),
        marker=dict(size=8),
        hovertemplate="Crime Score: %{y:.1f}<br>Borough: %{x}<extra></extra>",
        yaxis="y1"
    ))

    # Tourism Revenue 線圖
    fig.add_trace(go.Scatter(
        x=df["borough_name"],
        y=df["tourist_revenue"],
        mode="lines+markers",
        name="Tourism Revenue",
        line=dict(color="#EA7500", width=2),
        marker=dict(size=8),
        hovertemplate="Tourism Revenue: $%{y}M<br>Borough: %{x}<extra></extra>",
        yaxis="y2"
    ))

    # 平均 Crime Score 虛線
    fig.add_trace(go.Scatter(
        x=df["borough_name"],
        y=[avg_crime_score] * len(df),
        mode="lines",
        name="Avg Crime Score",
        line=dict(color="#8C4A2F", dash="dash", width=1.5),
        hovertemplate="Avg Crime Score: %{y:.1f}<extra></extra>",
        yaxis="y1",
        showlegend=True
    ))

    # 平均 Tourism Revenue 虛線
    fig.add_trace(go.Scatter(
        x=df["borough_name"],
        y=[avg_tourist_revenue] * len(df),
        mode="lines",
        name="Avg Tourism Revenue",
        line=dict(color="#B5651D", dash="dash", width=1.5),
        hovertemplate="Avg Tourism Revenue: $%{y}M<extra></extra>",
        yaxis="y2",
        showlegend=True
    ))

    # 更新佈局
    fig.update_layout(
        title=dict(
            text="Tourism Revenue vs. Crime Score",
            font=dict(size=18),
            x=0.5,
            xanchor='center',
            y=0.973
        ),
        yaxis=dict(
            title="Crime Score",
            side="left",
            showgrid=True,
            gridcolor="rgba(150, 150, 150, 0.35)",
            range=[0, max(df["crime_score"]) * 1.1]  # 動態設置範圍
        ),
        yaxis2=dict(
            title="Tourism Revenue (Millions $)",
            overlaying="y",
            side="right",
            showgrid=False,
            tickformat="$,.0f"
        ),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            tracegroupgap=50
        ),
        template="plotly_white",
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        hovermode='x unified'
    )

    return fig

# 測試用主程式
if __name__ == "__main__":
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H2("NYC Tourism Revenue vs. Crime Score",
                style={'text-align': 'left'}),
        dcc.Graph(
            figure=create_potential_figure(),
            config={"displayModeBar": False}
        )
    ])
    
    app.run_server(debug=True)