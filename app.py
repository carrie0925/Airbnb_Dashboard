import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
from fig_map import create_map_figure
from fig_price import create_price_figure
from fig_crime import create_crime_figure
from fig_potential import create_potential_figure
from fig_room import create_room_figure
from PIL import Image
from dotenv import load_dotenv
import os
import json

app = dash.Dash(__name__)
server = app.server

# 環境變數設置
dotenv_path = os.getenv("DOTENV_PATH")
load_dotenv(dotenv_path=dotenv_path)
logo_path = os.getenv("LOGO_PATH")
nyc_path = os.getenv("NYC_PATH")

logo_path = Image.open(logo_path)
nyc_path = Image.open(nyc_path)

# 顏色定義
colors = {
    "background": "#f5f5f5",
    "white": "white",
    "header": "#87CEFA",
}

BOROUGH_COLORS = {
    "Manhattan": "#ff928b",
    "Brooklyn": "#efe9ae",
    "Queens": "#cdeac0",
    "Bronx": "#ffac81",
    "Staten Island": "#fec3a6"
}

app.layout = html.Div([
    # 主容器
    html.Div([
        # 第一區塊：標題和 logo
        html.Div([
            html.Div([
                html.Img(
                    src=logo_path,
                    style={"height": "40px"}
                ),
                html.Img(
                    src=nyc_path,
                    style={"height": "40px"}
                ),
                html.H1("Airbnb New York City Listing Info", style={
                    "color": "gray",
                    "margin": "0",
                    "fontSize": "24px"
                })
            ], style={"display": "flex", "alignItems": "center", "gap": "15px"})
        ], style={
            "backgroundColor": "white",
            "padding": "7px",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            "borderRadius": "10px",
            "marginBottom": "20px"
        }),

        # 第二區塊：內容
        html.Div([
            # 右側：地圖和互動區域
            html.Div([
                # 地圖
                html.Div([
                    html.H3("New York City Map", style={
                        "color": "gray",
                        "textAlign": "center",
                        "marginBottom": "10px",
                        "marginTop": "1px",
                        "fontSize": "18px"
                    }),
                    dcc.Graph(
                        id='nyc-map',
                        figure=create_map_figure(),
                        config={"displayModeBar": False},
                        style={
                            "height": "256px",
                            "width": "320px",
                            "margin": "auto"
                        }
                    )
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "borderRadius": "10px",
                    "marginBottom": "20px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "width":"340px",
                    "height":"310px"
                }),

                # 互動結果
                html.Div([
                    html.H3("Selected Boroughs", style={
                        "color": "gray",
                        "textAlign": "center",
                        "marginBottom": "10px",
                        "marginTop": "1px",
                        "fontSize": "18px"
                    }),
                    html.Div(id="selected-boroughs", style={
                        "backgroundColor": "white",
                        "padding": "15px",
                        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                        "borderRadius": "10px",
                        "height": "300px",
                        "overflowY": "auto",
                        "overflowX":"hidden",
                        "width": "340px"
                    }),
                    dcc.Store(id='selected-boroughs-store', data=[])
                ])
            ], style={
                "width": "25%",
                "paddingRight": "20px",  # 修改為右側內邊距
                "display": "flex",
                "flexDirection": "column"
            }),

            # 左側：4 張圖表
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='price-graph',
                        figure=create_price_figure(),
                        config={"displayModeBar": False,},
                        style={"height": "370px", "width": "550px", "marginBottom": "20px"}
                    ),
                    dcc.Graph(
                        figure=create_crime_figure(),
                        config={"displayModeBar": False},
                        style={"height": "370px", "width": "550px", "marginBottom": "20px"}
                    )
                ], style={"display": "flex", "gap": "30px"}),

                html.Div([
                    dcc.Graph(
                        id='room-graph',
                        figure=create_room_figure(),
                        config={"displayModeBar": False},
                        style={"height": "370px", "width": "550px", "marginBottom": "20px"}
                    ),
                    dcc.Graph(
                        figure=create_potential_figure(),
                        config={"displayModeBar": False},
                        style={"height": "370px", "width": "550px", "marginBottom": "20px"}
                    )
                ], style={"display": "flex", "gap": "30px"})
            ], style={"display": "flex", "flexDirection": "column", "gap": "20px"})
        ], style={
            "display": "flex",
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"
        })

    ], style={
        "maxWidth": "1800px",
        "margin": "0 auto",
        "padding": "20px"
    })
], style={
    "backgroundColor": "#f5f5f5",
    "minHeight": "100vh"
})

def generate_borough_cards(boroughs):
    if not boroughs:
        return html.Div("Click on boroughs to see details", 
                       style={"textAlign": "center", "color": "#666"})
    
    return html.Div([
        html.Div([
            html.Div([
                html.Button(
                    "×",
                    id={'type': 'close-button', 'index': b['name']},
                    style={
                        'position': 'absolute',
                        'right': '10px',
                        'top': '10px',
                        'background': 'none',
                        'border': 'none',
                        'fontSize': '20px',
                        'cursor': 'pointer',
                        'color': '#666'
                    }
                ),
                html.H4(b['name'], style={
                    'margin': '0 0 10px 0',
                    'color': '#333',
                    'fontSize': '17px'
                }),
                html.P([
                    "Total Listings: ", 
                    html.Strong(f"{b['listings']:,}")
                ], style={'margin': '5px 0','fontSize':'14px'}),
                html.P([
                    "Expected Tourism Value: ", 
                    html.Strong(f"${b['tourism']:,}M")
                ], style={'margin': '5px 0', 'fontSize': '14px'}),
                 html.P([  
                    "Crime Rank: ", 
                    html.Strong(f"{b['crime_rank']}")
                ], style={'margin': '5px 0', 'fontSize': '14px'}),
                html.P([  
                    "Investment Rank: ", 
                    html.Strong(f"{b['investment_rank']}")
                ], style={'margin': '5px 0', 'fontSize': '14px','color': '#FF4500','fontWeight': 'bold','fontSize': '17px','textDecoration':'underline'})
            ], style={
                'position': 'relative',
                'padding': '10px',
                'marginBottom': '7px',
                'borderRadius': '8px',
                'backgroundColor': BOROUGH_COLORS[b['name']],
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width':'90%',
                'margin':'0 auto 10px auto'
            })
        ]) for b in boroughs
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '5px', 'maxHeight': '280px','overflowY':'auto'})

@app.callback(
    [Output('selected-boroughs-store', 'data'),
     Output('selected-boroughs', 'children'),
     Output('price-graph', 'figure'),
     Output('room-graph', 'figure')],
    [Input('nyc-map', 'clickData')],
    [State('selected-boroughs-store', 'data')]
)
def update_selected_boroughs(clickData, current_selections):
    if clickData is None:
        return current_selections, generate_borough_cards(current_selections), create_price_figure(), create_room_figure()
    
    # 獲取點擊的區域名稱及相關數據
    clicked_borough = clickData['points'][0]['customdata'][0]
    listings_count = clickData['points'][0]['customdata'][1]
    tourism_value = clickData['points'][0]['customdata'][2]

    # 加入排名資訊
    borough_ranks = {
        "Brooklyn": {"investment_rank": 5, "crime_rank": 1},
        "Manhattan": {"investment_rank": 1, "crime_rank": 4},
        "Queens": {"investment_rank": 2, "crime_rank": 3},
        "Bronx": {"investment_rank": 4, "crime_rank": 2},
        "Staten Island": {"investment_rank": 3, "crime_rank": 5}
    }
    
    # 根據地區獲取排名
    investment_rank = borough_ranks[clicked_borough]["investment_rank"]
    crime_rank = borough_ranks[clicked_borough]["crime_rank"]
    
    # 整合資料
    borough_data = {
        'name': clicked_borough,
        'listings': listings_count,
        'tourism': tourism_value,
        'crime_rank': crime_rank,
        'investment_rank': investment_rank
    }
    
    # 檢查是否已存在於選定列表中
    if current_selections is None:
        current_selections = []
    
    if any(b['name'] == clicked_borough for b in current_selections):
        # 如果存在，移除該地區
        current_selections = [b for b in current_selections if b['name'] != clicked_borough]
    else:
        # 如果不存在，新增地區資訊
        current_selections.append(borough_data)
    
    # 更新卡片和圖表
    cards = generate_borough_cards(current_selections)
    price_fig = create_price_figure([b['name'] for b in current_selections])
    room_fig = create_room_figure([b['name'] for b in current_selections])
    
    return current_selections, cards, price_fig, room_fig

@app.callback(
    [Output('selected-boroughs-store', 'data', allow_duplicate=True),
     Output('selected-boroughs', 'children', allow_duplicate=True),
     Output('price-graph', 'figure', allow_duplicate=True),
     Output('room-graph', 'figure', allow_duplicate=True)],
    [Input({'type': 'close-button', 'index': ALL}, 'n_clicks')],
    [State('selected-boroughs-store', 'data')],
    prevent_initial_call=True
)
def remove_borough_card(n_clicks, current_selections):
    if not any(n_clicks):
        raise dash.exceptions.PreventUpdate
    
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    borough_to_remove = button_id['index']
    
    updated_selections = [b for b in current_selections if b['name'] != borough_to_remove]
    selected_borough_names = [b['name'] for b in updated_selections]
    
    # Create updated figures
    price_fig = create_price_figure(selected_borough_names)
    room_fig = create_room_figure(selected_borough_names)
    
    cards = generate_borough_cards(updated_selections)
    
    # 修正：返回所有四個值
    return updated_selections, cards, price_fig, room_fig

if __name__ == '__main__':
    app.run_server(debug=True)