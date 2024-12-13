import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import os
import base64

def create_map_figure():
    """創建地圖圖表的函數"""
    # 讀取地圖背景圖片
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'assets', 'images', 'map_final.jpg')
    
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    
    # 創建數據
    borough_data = {
        "Manhattan": {"listings_count": 8038, "tourism_value": 32831},
        "Brooklyn": {"listings_count": 7717, "tourism_value": 2973},
        "Queens": {"listings_count": 3753, "tourism_value": 9938},
        "Bronx": {"listings_count": 948, "tourism_value": 955},
        "Staten Island": {"listings_count": 373, "tourism_value": 456}
    }

    # 五大行政區的位置
    positions = {
        "Bronx": (290, 86),
        "Brooklyn": (230, 290),
        "Manhattan": (188, 172),
        "Queens": (360, 200),
        "Staten Island": (100, 344)
    }

    # 建立 Plotly 地圖
    fig_map = go.Figure()

    # 設定背景圖片
    fig_map.update_layout(
        images=[dict(
            source=f'data:image/jpg;base64,{encoded_image}',
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            sizing="contain",  # 改為 "contain" 以保持長寬比
            opacity=1,
            layer="below"
        )]
    )

    # 添加行政區互動點
    for borough, pos in positions.items():
        data = borough_data[borough]
        listings_count = data["listings_count"]
        tourism_value = data["tourism_value"]
        
        hover_text = (
            f"<b>{borough}</b><br>"
            f"Total Listing Count: {listings_count:,}<br>"
            f"Expected Tourism Value: ${tourism_value:,}M"
        )
        
        fig_map.add_trace(
            go.Scatter(
                x=[pos[0]],
                y=[400 - pos[1]],
                mode="markers",
                marker=dict(
                    size=12,
                    color="darkred",
                    symbol="circle",
                ),
                hoverinfo="text",
                hovertext=hover_text,
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="black",
                    font=dict(size=12)
                ),
                customdata=[[borough, listings_count, tourism_value]],
                name=borough
            )
        )

    # 更新布局設定
    fig_map.update_layout(
        xaxis=dict(
            range=[0, 500],
            showgrid=False,
            zeroline=False,
            visible=False,
            scaleanchor="y",  # 鎖定與 y 軸的比例
            constrain="domain"
        ),
        yaxis=dict(
            range=[0, 400],
            showgrid=False,
            zeroline=False,
            visible=False,
            constrain="domain"
        ),
        showlegend=False,
        template="plotly_white",
        width=500,           # 增加寬度
        height=400,          # 增加高度並保持比例
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hoverdistance=5,
        hovermode='closest',
        clickmode='event'
    )
    
    return fig_map

# 如果直接運行此文件，則啟動獨立的 Dash 應用
if __name__ == "__main__":
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("紐約市五大行政區互動地圖", style={"text-align": "center"}),
        dcc.Graph(
            id="interactive-map",
            figure=create_map_figure(),
            config={"displayModeBar": False},
            style={"width": "700px", "height": "560px", "margin": "auto"}  # 調整顯示尺寸
        )
    ])
    app.run_server(debug=True)