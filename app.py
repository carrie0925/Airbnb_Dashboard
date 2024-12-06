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
        # 左側區塊：地圖和互動區域
        html.Div([
            # 標題、地圖和互動區域的容器
            html.Div([
                # 標題和 logo
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
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "15px",
                    "marginBottom": "20px",
                    "width": "500px"
                }),
                
                # 地圖區域
                html.Div([
                    html.H3("Click dots to see details", style={
                        "color": "darkred",
                        "textAlign": "center",
                        "marginBottom": "10px",
                        "marginTop": "1px",
                        "fontSize": "20px"
                    }),
                    # html.P("Click dots to see details", style={
                    #     "textAlign": "center",
                    #     "color": "darkred",
                    #     "fontSize": "14px",
                    #     "marginBottom": "10px"
                    # }),
                    dcc.Graph(
                        id='nyc-map',
                        figure=create_map_figure(),
                        config={"displayModeBar": False},
                        style={
                            "height": "400px",
                            "width": "100%",
                            "margin": "50px"
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
                    "width": "500px"
                }),

                # Selected Boroughs 區域
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
                        "overflowX": "hidden",
                        "width": "470px"
                    }),
                    dcc.Store(id='selected-boroughs-store', data=[])
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "10px",
                    "width": "500px"
                })
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                "width": "540px"
            })
        ], style={
            "paddingRight": "20px"
        }),

        # 右側區塊：資訊總覽和圖表
        html.Div([
            # 總覽資訊
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Year", style={"margin": "0", "color": "gray"}),
                        html.H2("2024", style={"margin": "5px 0", "color": "#333"})
                    ], style={"textAlign": "center", "flex": "1"}),
                    html.Div([
                        html.H3("Total Listings", style={"margin": "0", "color": "gray"}),
                        html.H2("20,747", style={"margin": "5px 0", "color": "#333"})
                    ], style={"textAlign": "center", "flex": "1"}),
                    html.Div([
                        html.H3("Best Investment Area", style={"margin": "0", "color": "gray"}),
                        html.H2(id="best-investment-area", 
                                children="Manhattan",  # 默認值
                                style={"margin": "5px 0", "color": "#FF4500"})
                    ], style={"textAlign": "center", "flex": "1"})
                ], style={
                    "display": "flex",
                    "justifyContent": "space-around",
                    "padding": "20px",
                    "backgroundColor": "white",
                    "borderRadius": "10px",
                    "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "marginBottom": "20px"
                })
            ]),

            # 圖表區域
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='price-graph',
                        figure=create_price_figure(),
                        config={"displayModeBar": False},
                        style={"height": "450px", "width": "550px"}
                    ),
                    dcc.Graph(
                        figure=create_crime_figure(),
                        config={"displayModeBar": False},
                        style={"height": "450px", "width": "550px"}
                    )
                ], style={"display": "flex", "gap": "30px", "marginBottom": "30px"}),

                html.Div([
                    dcc.Graph(
                        id='room-graph',
                        figure=create_room_figure(),
                        config={"displayModeBar": False},
                        style={"height": "450px", "width": "550px"}
                    ),
                    dcc.Graph(
                        figure=create_potential_figure(),
                        config={"displayModeBar": False},
                        style={"height": "450px", "width": "550px"}
                    )
                ], style={"display": "flex", "gap": "30px"})
            ])
        ], style={
            "flex": "1",
            "display": "flex",
            "flexDirection": "column"
        })
    ], style={
        "display": "flex",
        "backgroundColor": "white",
        "padding": "20px",
        "borderRadius": "10px",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
        "maxWidth": "1800px",
        "margin": "0 auto",
        "gap": "20px"
    })
], style={
    "backgroundColor": "#f5f5f5",
    "minHeight": "100vh",
    "padding": "20px"
})

def generate_borough_cards(boroughs):
    if not boroughs:
        return html.Div("Click on boroughs to see details", 
                       style={"textAlign": "center", "color": "#666"})
    
    def get_dollar_signs(rank):
        return "".join(["$" for _ in range(6 - rank)])

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
                ], style={'margin': '5px 0', 'fontSize': '14px'}),
                html.P([
                    "Expected Tourism Value: ", 
                    html.Strong(f"${b['tourism']:,}M")
                ], style={'margin': '5px 0', 'fontSize': '14px'}),
                html.P([  
                    "Crime Rank: ", 
                    html.Strong(f"{b['crime_rank']}")
                ], style={'margin': '5px 0', 'fontSize': '14px'}),
                # Investment Rank 的新佈局
                html.Div([
                    html.Div([
                        "Investment Rank: ",
                        html.Strong(f"{b['investment_rank']}")
                    ], style={
                        'flex': '1',
                        'margin': '5px 0',
                        'fontSize': '17px',
                        'color': '#FF4500',
                        'fontWeight': 'bold',
                        'textDecoration': 'underline'
                    }),
                    # html.Div(
                    #     get_dollar_signs(b['investment_rank']),
                    #     style={
                    #         'flex': '1',
                    #         'color': '#FFD700',
                    #         'textShadow': '1px 1px 1px rgba(0,0,0,0.2)',
                    #         'fontSize': '20px',
                    #         'textAlign': 'right',
                    #         'paddingRight': '10px'
                    #     }
                    # )
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'space-between',
                    'width': '100%'
                })
            ], style={
                'position': 'relative',
                'padding': '15px',
                'marginBottom': '10px',
                'borderRadius': '8px',
                'backgroundColor': BOROUGH_COLORS[b['name']],
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'width': '95%',
                'margin': '0 auto'
            })
        ]) for b in boroughs
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '5px',
        'maxHeight': '280px',
        'overflowY': 'auto',
        'width': '100%'
    })

@app.callback(
    [Output('selected-boroughs-store', 'data'),
     Output('selected-boroughs', 'children'),
     Output('price-graph', 'figure'),
     Output('room-graph', 'figure'),
     Output('best-investment-area', 'children')],
    [Input('nyc-map', 'clickData')],
    [State('selected-boroughs-store', 'data')]
)
def update_selected_boroughs(clickData, current_selections):
    best_investment = "Manhattan"

    if clickData is None:
        return  (
            current_selections,
            generate_borough_cards(current_selections),
            create_price_figure(),
            create_room_figure(),
            best_investment
        )
    
    clicked_borough = clickData['points'][0]['customdata'][0]
    listings_count = clickData['points'][0]['customdata'][1]
    tourism_value = clickData['points'][0]['customdata'][2]

    borough_ranks = {
        "Brooklyn": {"investment_rank": 5, "crime_rank": 1},
        "Manhattan": {"investment_rank": 1, "crime_rank": 4},
        "Queens": {"investment_rank": 2, "crime_rank": 3},
        "Bronx": {"investment_rank": 4, "crime_rank": 2},
        "Staten Island": {"investment_rank": 3, "crime_rank": 5}
    }
    
    investment_rank = borough_ranks[clicked_borough]["investment_rank"]
    crime_rank = borough_ranks[clicked_borough]["crime_rank"]
    
    borough_data = {
        'name': clicked_borough,
        'listings': listings_count,
        'tourism': tourism_value,
        'crime_rank': crime_rank,
        'investment_rank': investment_rank
    }
    
    if current_selections is None:
        current_selections = []
    
    if any(b['name'] == clicked_borough for b in current_selections):
        current_selections = [b for b in current_selections if b['name'] != clicked_borough]
    else:
        current_selections.append(borough_data)
    

    if current_selections:
        # 從選中的區域中找出投資排名最高的
        selected_ranks = {b['name']: borough_ranks[b['name']]["investment_rank"] 
                        for b in current_selections}
        best_investment = min(selected_ranks.items(), key=lambda x: x[1])[0]
    
    cards = generate_borough_cards(current_selections)
    price_fig = create_price_figure([b['name'] for b in current_selections])
    room_fig = create_room_figure([b['name'] for b in current_selections])
    
    return (
        current_selections,
        cards,
        price_fig,
        room_fig,
        best_investment
    )
    
@app.callback(
    [Output('selected-boroughs-store', 'data', allow_duplicate=True),
     Output('selected-boroughs', 'children', allow_duplicate=True),
     Output('price-graph', 'figure', allow_duplicate=True),
     Output('room-graph', 'figure', allow_duplicate=True),
     Output('best-investment-area', 'children', allow_duplicate=True)],
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
    
    # 找出最佳投資區域
    borough_ranks = {
        "Brooklyn": {"investment_rank": 5},
        "Manhattan": {"investment_rank": 1},
        "Queens": {"investment_rank": 2},
        "Bronx": {"investment_rank": 4},
        "Staten Island": {"investment_rank": 3}
    }
    best_investment = "Manhattan"  # 默認值
    if updated_selections:
        selected_ranks = {b['name']: borough_ranks[b['name']]["investment_rank"] 
                        for b in updated_selections}
        best_investment = min(selected_ranks.items(), key=lambda x: x[1])[0]

    price_fig = create_price_figure(selected_borough_names)
    room_fig = create_room_figure(selected_borough_names)
    cards = generate_borough_cards(updated_selections)
    
    return updated_selections, cards, price_fig, room_fig, best_investment

if __name__ == '__main__':
    app.run_server(debug=True)