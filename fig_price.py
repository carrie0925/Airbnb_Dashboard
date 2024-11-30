import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

def create_price_figure():
    """創建房價和房源數量分析圖表"""
    try:
        # 載入環境變數
        load_dotenv()
        
        # 資料庫連接與查詢
        db_path = os.getenv("DB_PATH")
        if not db_path:
            raise ValueError("DB_PATH environment variable not found")
            
        conn = sqlite3.connect(db_path)
        
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
            b.borough_name IN ('Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island')
            AND l.price IS NOT NULL
            AND l.price > 0
        GROUP BY 
            b.borough_name;
        """
        
        df = pd.read_sql_query(query, conn)
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
            x=df['borough'],
            y=df['NumberOfProperties'],
            marker_color=[borough_colors[borough] for borough in df['borough']],
            name='Number of Properties',
            yaxis='y',
            hovertemplate="Borough: %{x}<br>Properties: %{y:,}<extra></extra>"
        ))

        # 折線圖：平均價格（右側 Y 軸）
        fig.add_trace(go.Scatter(
            x=df['borough'],
            y=df['AveragePrice'],
            mode='lines+markers',
            line=dict(color='#333333', width=2),
            marker=dict(color='#000000', size=8),
            name='Average Price ($)',
            yaxis='y2',
            hovertemplate="Borough: %{x}<br>Avg Price: $%{y:,.2f}<extra></extra>"
        ))

        # 更新圖表格式
        fig.update_layout(
            title=dict(
                text="Average Price and Number of Properties by Borough",
                font=dict(size=20)
            ),
            xaxis=dict(
                title="Boroughs",
                titlefont=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="Number of Properties",
                titlefont=dict(color="#333333"),
                tickfont=dict(color="#333333", size=12),
                gridcolor='lightgray'
            ),
            yaxis2=dict(
                title="Average Price ($)",
                titlefont=dict(color="#333333"),
                tickfont=dict(color="#333333", size=12),
                overlaying="y",
                side="right",
                gridcolor='lightgray'
            ),
            legend=dict(
                title="Metrics",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
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

# 如果直接運行此文件，則啟動獨立的 Dash 應用
if __name__ == "__main__":
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H2("Price Analysis by Borough", 
                style={'text-align': 'center'}),
        dcc.Graph(figure=create_price_figure())
    ])
    
    app.run_server(debug=True)