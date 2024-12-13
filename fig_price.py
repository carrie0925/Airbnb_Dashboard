import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import os


def create_price_figure(selected_boroughs=None):
    """創建房價和房源數量分析圖表"""
    try:
        # 根據環境選擇資料庫路徑
        if os.environ.get('ENV') == 'production':
            db_path = os.environ.get('DATABASE_URL')  # Heroku 環境使用 DATABASE_URL
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, 'db_final.db')  # 本地開發環境使用 SQLite
        
        # 建立資料庫連線
        with sqlite3.connect(db_path) as conn:
            # 基本查詢
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
                borough b ON loc.borough_id = b.borough_id
            WHERE 
                l.price IS NOT NULL
                AND l.price > 0
            """

            # 添加篩選條件（如果有選擇）
            if selected_boroughs:
                borough_list = "', '".join(selected_boroughs)
                query += f" AND b.borough_name IN ('{borough_list}')"
            else:
                query += " AND b.borough_name IN ('Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island')"
            
            query += " GROUP BY b.borough_name;"
            
            # 執行查詢並讀取資料
            df = pd.read_sql_query(query, conn)

        # 自定義行政區域顏色
        borough_colors = {
            "Manhattan": "#ff928b",
            "Brooklyn": "#efe9ae",
            "Queens": "#cdeac0",
            "Bronx": "#ffac81",
            "Staten Island": "#fec3ab"
        }

        # 構造圖表
        fig = go.Figure()

        # 長條圖：房源數量（左側 Y 軸）
        fig.add_trace(go.Bar(
            x=df['borough'],
            y=df['NumberOfProperties'],
            marker_color=[borough_colors[borough] for borough in df['borough']],
            name='Number of Properties',
            yaxis='y',
            showlegend=False,
            hovertemplate="Borough: %{x}<br>Properties: %{y:,}<extra></extra>"
        ))

        # 折線圖：平均價格（右側 Y 軸）
        fig.add_trace(go.Scatter(
            x=df['borough'],
            y=df['AveragePrice'],
            mode='lines+markers',
            line=dict(color='gray', width=2),
            marker=dict(color='gray', size=6),
            name='Average Price ($)',
            yaxis='y2',
            showlegend=False,
            hovertemplate="Borough: %{x}<br>Avg Price: $%{y:,.2f}<extra></extra>"
        ))

        # 更新圖表格式
        fig.update_layout(
            title=dict(
                text="Average Price & Property Count by Borough",
                x=0.5,
                font=dict(size=18)
            ),
            yaxis=dict(
                title="Number of Properties",
                titlefont=dict(color="#333333"),
                tickfont=dict(color="#333333", size=12),
                gridcolor='rgba(150, 150, 150, 0.35)'
            ),
            yaxis2=dict(
                title="Average Price ($)",
                titlefont=dict(color="#333333"),
                tickfont=dict(color="#333333", size=12),
                overlaying="y",
                side="right",
                showgrid=False,
                zeroline=False,
                tickformat="$,.0f"  # 添加美元符號和千位分隔符
            ),
            showlegend=False,
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            hovermode='x unified'  # 改善 hover 效果
        )

        return fig

    except Exception as e:
        print(f"Error creating price figure: {e}")
        fig = go.Figure()
        fig.update_layout(
            title="Error Loading Price Data",
            annotations=[{
                "text": "Error loading price data. Please check database connection.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 14}
            }]
        )
        return fig


# 測試用主程式
if __name__ == "__main__":
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H2("Price Analysis by Borough", 
                style={'text-align': 'center'}),
        dcc.Graph(
            figure=create_price_figure(),
            config={"displayModeBar": False}
        )
    ])
    app.run_server(debug=True)
