import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from dotenv import load_dotenv
import os

def create_crime_figure():
    """創建犯罪分布堆疊百分比柱狀圖"""
    try:
        # 載入環境變數
        load_dotenv()
        
        # 資料庫連接與查詢
        db_path = os.getenv("DB_PATH")
        if not db_path:
            raise ValueError("DB_PATH environment variable not found")
            
        conn = sqlite3.connect(db_path)
        
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
            BoroughTotals b ON c.borough = b.borough;
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()

        # 確保資料框內有資料
        if df.empty:
            raise ValueError("Database query returned no results")

        # 轉換資料以適應堆疊長條圖
        pivot_df = df.pivot(index="borough", columns="crime_type", values="crime_count").fillna(0)
        pivot_pct = df.pivot(index="borough", columns="crime_type", values="crime_percentage").fillna(0)

        # 定義自訂顏色
        custom_colors = {
            "VIOLATION": "#F5D3B3",
            "MISDEMEANOR": "#EBC2A0",
            "FELONY": "#D9A679"
        }

        # 繪製堆疊長條圖
        fig = go.Figure()

        # 計算累積值以確定標籤位置
        y_positions = {borough: 0 for borough in pivot_df.index}

        for crime_type in pivot_df.columns:
            counts = pivot_df[crime_type]
            percentages = pivot_pct[crime_type]
            
            fig.add_trace(go.Bar(
                x=pivot_df.index,
                y=counts,
                name=crime_type,
                marker=dict(color=custom_colors[crime_type]),
                text=[f"{pct:.1f}%" for pct in percentages],  # 添加百分比標籤
                textposition="inside",  # 在長條圖內顯示標籤
                insidetextanchor="middle",  # 標籤置中
                textfont=dict(
                    color="black",
                    size=11
                ),
                hovertemplate="Borough: %{x}<br>" +
                            "Crime Type: " + crime_type + "<br>" +
                            "Count: %{y:,}<br>" +
                            "<extra></extra>",
            ))

        # 更新佈局
        fig.update_layout(
            title=dict(
                text="Distribution of Crime Types by Borough",
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            barmode="stack",
            yaxis=dict(
                title="Crime Count",
                tickfont=dict(size=12),
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGrey'
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(size=11),
            ),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=True,
            uniformtext=dict(mode="hide", minsize=10)  # 控制標籤的顯示
        )

        return fig
    
    except Exception as e:
        print(f"Error creating crime figure: {e}")
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