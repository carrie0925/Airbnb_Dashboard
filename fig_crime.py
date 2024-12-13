import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import os
import psycopg2

def get_db_connection():
    """根據環境返回正確的資料庫連線"""
    if os.environ.get('ENV') == 'production':
        # 使用 PostgreSQL 連線
        DATABASE_URL = os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        # 使用 SQLite 在本地開發環境
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_final.db')
        conn = sqlite3.connect(db_path)
    return conn

def create_crime_figure():
    """創建犯罪分布堆疊百分比柱狀圖"""
    query = """
    WITH CrimeCounts AS (
        SELECT 
            b.borough_name AS borough,
            s.crime_level AS crime_type,
            COUNT(s.Event_id) AS crime_count
        FROM 
            borough b
        LEFT JOIN 
            security s ON b.borough_id = s.borough_id
        GROUP BY 
            b.borough_id, b.borough_name, s.crime_level
    ),
    BoroughTotals AS (
        SELECT 
            borough,
            SUM(crime_count) as total_crimes
        FROM 
            CrimeCounts
        GROUP BY 
            borough
    )
    SELECT 
        c.borough,
        c.crime_type,
        c.crime_count,
        CAST(c.crime_count AS FLOAT) / b.total_crimes * 100 as crime_percentage
    FROM 
        CrimeCounts c
    JOIN 
        BoroughTotals b ON c.borough = b.borough
    ORDER BY c.borough;
    """
    try:
        conn = get_db_connection()

        df = pd.read_sql_query(query, conn)
        if df.empty:
            raise ValueError("Database query returned no results")

        df = df.dropna(subset=["borough", "crime_type"])
        pivot_df = df.pivot(index="borough", columns="crime_type", values="crime_count").fillna(0)
        pivot_pct = df.pivot(index="borough", columns="crime_type", values="crime_percentage").fillna(0)

        # 定義自訂顏色
        custom_colors = {
            "VIOLATION": "#FFD1A4",     # 淺橘
            "MISDEMEANOR": "#E3A887",   # 中橘
            "FELONY": "#C17767"         # 深橘
        }

        # 繪製堆疊長條圖
        fig = go.Figure()

        for crime_type in pivot_df.columns:
            counts = pivot_df[crime_type]
            percentages = pivot_pct[crime_type]
            
            fig.add_trace(go.Bar(
                x=pivot_df.index,
                y=counts,
                name=crime_type.title(),  # 首字母大寫
                marker=dict(color=custom_colors[crime_type]),
                text=[f"{pct:.1f}%" for pct in percentages],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(
                    color="black",
                    size=11
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>" +
                    f"Crime Type: {crime_type.title()}<br>" +
                    "Count: %{y:,}<br>" +
                    "Percentage: %{text}<br>" +
                    "<extra></extra>"
                )
            ))

        # 更新佈局
        fig.update_layout(
            title=dict(
                text="Distribution of Crime Types by Borough",
                x=0.5,
                font=dict(size=18)
            ),
            barmode="stack",
            yaxis=dict(
                title="Number of Crimes",
                titlefont=dict(size=14),
                tickfont=dict(size=12),
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(150, 150, 150, 0.35)',
                tickformat=",d"  # 添加千位分隔符
            ),
            xaxis=dict(
                title="Borough",
                titlefont=dict(size=14),
                tickfont=dict(size=12)
            ),
            legend=dict(
                title="Crime Type",
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=80, b=80),
            showlegend=True,
            uniformtext=dict(mode="hide", minsize=10),
            plot_bgcolor="white",
            hovermode='closest'
        )

        return fig
    
    except Exception as e:
        print(f"Error creating crime figure: {e}")
        return go.Figure().update_layout(
            title="Error Loading Data",
            annotations=[{
                "text": "Error loading data. Please check database connection.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 14}
            }]
        )
    finally:
        conn.close()  

# 測試用主程式
if __name__ == "__main__":
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H2("NYC Crime Distribution Analysis", 
                style={'text-align': 'center', 'color': '#333'}),
        dcc.Graph(
            figure=create_crime_figure(),
            config={"displayModeBar": False}
        )
    ])
    
    app.run_server(debug=True)