import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import sqlite3
import os

def create_room_figure(selected_boroughs=None, y_range=None):
    """創建房型分析箱型圖"""
    try:
        # 獲取資料庫路徑
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
                l.listing_id,
                h.host_name,
                l.room_type,
                l.price
            FROM 
                listings l
            JOIN 
                locations loc ON l.listing_id = loc.listing_id
            JOIN 
                borough b ON loc.borough_id = b.borough_id
            JOIN
                hosts h ON l.host_id = h.host_id
            WHERE 
                l.price > 0 
                AND l.price < 2000
            """

            # 添加行政區篩選條件（如果有選擇）
            if selected_boroughs:
                borough_list = "', '".join(selected_boroughs)
                query += f" AND b.borough_name IN ('{borough_list}')"

            df = pd.read_sql_query(query, conn)

        # 過濾和重命名房型類型
        room_type_mapping = {
            "Private room": "Private Room",
            "Entire home/apt": "Entire Home/Apt",
            "Hotel room": "Hotel Room",
            "Shared room": "Shared Room"
        }
        df = df[df["room_type"].isin(room_type_mapping.keys())]
        df["room_type"] = df["room_type"].map(room_type_mapping)

        # 自定義色票（還原您的原始配色）
        custom_colors = {
            "Private Room": "#9c9c7c",
            "Entire Home/Apt": "#9c9c7c",
            "Hotel Room": "#9c9c7c",
            "Shared Room": "#9c9c7c"
        }

        # 創建箱型圖
        fig = px.box(
            df,
            x="room_type",
            y="price",
            title="Price Distribution by Room Type",
            labels={
                "room_type": "Room Type",
                "price": "Price per Night ($)"
            },
            color="room_type",
            color_discrete_map=custom_colors,
            hover_data=["listing_id", "host_name"]
        )

        # 設定 y 軸範圍
        y_axis_range = y_range if y_range else [0, min(2000, df['price'].quantile(0.95))]

        # 更新圖表佈局
        fig.update_layout(
            showlegend=False,
            yaxis=dict(
                range=y_axis_range,
                title=dict(text="Price per Night ($)", font=dict(size=14)),
                gridcolor="rgba(150, 150, 150, 0.35)",
                tickprefix="$",
                tickfont=dict(size=12)
            ),
            xaxis=dict(
                title=dict(text="Room Type", font=dict(size=14)),
                tickfont=dict(size=12),
                categoryorder="total ascending"
            ),
            title=dict(
                text="Room Type Price Distribution",
                font=dict(size=18),
                x=0.5
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=450,
            margin=dict(t=50, b=80, l=50, r=50),
            hovermode="closest"
        )

        # 更新箱型圖的 hover 效果
        fig.update_traces(
            boxmean=True,  # 顯示平均值
            hovertemplate=(
                "<b>%{x}</b><br>" +
                "Price: $%{y:,.2f}<br>" +
                "Host: %{customdata[1]}<br>" +
                "Listing ID: %{customdata[0]}" +
                "<extra></extra>"
            )
        )

        return fig

    except Exception as e:
        print(f"Error creating room figure: {e}")
        return px.box(
            pd.DataFrame({'x': [], 'y': []}),
            title="Error Loading Data"
        ).add_annotation(
            text="Error loading data. Please check database connection.",
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=14)
        )

# 測試用主程式
if __name__ == "__main__":
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H2("Room Type Analysis", 
                style={'text-align': 'center', 'margin-bottom': '20px'}),
        
        # 行政區選擇
        html.Div([
            html.Label("Select Boroughs:", style={
                'fontSize': '16px',
                'fontWeight': 'bold',
                'marginBottom': '10px',
                'color': '#333'
            }),
            dcc.Checklist(
                id="borough-checklist",
                options=[
                    {"label": " Manhattan", "value": "Manhattan"},
                    {"label": " Brooklyn", "value": "Brooklyn"},
                    {"label": " Queens", "value": "Queens"},
                    {"label": " Bronx", "value": "Bronx"},
                    {"label": " Staten Island", "value": "Staten Island"}
                ],
                value=[],
                inline=True,
                style={'fontSize': '14px', 'margin': '10px'}
            )
        ], style={
            'padding': '20px',
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'marginBottom': '20px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }),

        # 價格範圍選擇
        html.Div([
            html.Label("Select Price Range:", style={
                'fontSize': '16px',
                'fontWeight': 'bold',
                'marginBottom': '10px',
                'color': '#333'
            }),
            dcc.RangeSlider(
                id='price-range-slider',
                min=0,
                max=2000,
                step=100,
                marks={
                    0: '$0',
                    500: '$500',
                    1000: '$1,000',
                    1500: '$1,500',
                    2000: '$2,000'
                },
                value=[0, 2000]
            )
        ], style={
            'padding': '20px',
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'marginBottom': '20px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }),
        
        dcc.Graph(
            id="boxplot-graph",
            figure=create_room_figure(),
            config={"displayModeBar": False}
        )
    ], style={
        'padding': '20px',
        'backgroundColor': '#f5f5f5'
    })
    
    @app.callback(
        Output("boxplot-graph", "figure"),
        [Input("borough-checklist", "value"),
         Input("price-range-slider", "value")]
    )
    def update_boxplot(selected_boroughs, price_range):
        return create_room_figure(
            selected_boroughs=selected_boroughs,
            y_range=price_range
        )
    
    app.run_server(debug=True)
