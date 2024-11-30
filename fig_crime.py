import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

def create_crime_figure():
    """創建犯罪分布堆疊柱狀圖"""
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
            raise ValueError("Database query returned no results")

        # 轉換資料以適應堆疊長條圖
        pivot_df = df.pivot(index="borough", columns="crime_type", values="crime_count").fillna(0)

        # 定義自訂顏色
        custom_colors = {
            "VIOLATION": "#ceba6e",
            "MISDEMEANOR": "#909880",
            "FELONY": "#909c54"
        }

        # 繪製堆疊長條圖
        fig = go.Figure()

        for crime_type in pivot_df.columns:
            fig.add_trace(go.Bar(
                x=pivot_df.index,
                y=pivot_df[crime_type],
                name=crime_type,
                marker=dict(color=custom_colors[crime_type]),
                hovertemplate="Crime Type: %{x}<br>Count: %{y}<br><extra></extra>",
            ))

        # 更新佈局
        fig.update_layout(
            title="Distribution of Crime Types by Borough",
            barmode="stack",
            xaxis=dict(
                title="Borough",
                tickfont=dict(size=12),
            ),
            yaxis=dict(
                title="Crime Count",
                tickvals=[0, 20000, 40000, 60000, 80000, 100000, 120000],
                tickformat="",
                tickfont=dict(size=12),
            ),
            legend=dict(
                title="Crime Type",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=10),  # 字體大小
                tracegroupgap=50
            ),
            template="plotly_white",
            height=400,  # 固定高度
            margin=dict(l=50, r=50, t=80, b=50)  # 調整邊距
        )

        return fig
    
    except Exception as e:
        print(f"Error creating crime figure: {e}")
        # 返回一個空的圖表而不是失敗
        fig = go.Figure()
        fig.update_layout(
            title="Error Loading Crime Data",
            annotations=[{
                "text": "Error loading crime data. Please check database connection.",
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
        html.H2("Distribution of Crime Types in New York City", 
                style={'text-align': 'center'}),
        dcc.Graph(figure=create_crime_figure())
    ])
    
    app.run_server(debug=True)