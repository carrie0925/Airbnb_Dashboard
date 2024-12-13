import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
from fig_map import create_map_figure
from fig_price import create_price_figure
from fig_crime import create_crime_figure
from fig_potential import create_potential_figure
from fig_room import create_room_figure
from PIL import Image
# from dotenv import load_dotenv
import os
import json

app = dash.Dash(__name__,assets_folder='assets')
server = app.server

# 環境變數設置
# dotenv_path = os.getenv("DOTENV_PATH")
# load_dotenv(dotenv_path=dotenv_path)

# logo_path = "image/airbnb_logo.png"
# nyc_path = "image/Flag_of_New_York_City.png"
# borough_image_path = "image"


# logo_path = Image.open(logo_path)
# nyc_path = Image.open(nyc_path)
# borough_images = {
#     "Manhattan": Image.open(os.path.join(borough_image_path, "Manhaton.jpg")),
#     "Brooklyn": Image.open(os.path.join(borough_image_path, "Brooklyn.jpg")),
#     "Queens": Image.open(os.path.join(borough_image_path, "Queens.jpg")),
#     "Bronx": Image.open(os.path.join(borough_image_path, "Bronx.jpg")),
#     "Staten Island": Image.open(os.path.join(borough_image_path, "Staten_Island.jpg"))
# }


logo_path = app.get_asset_url('images/airbnb_logo.png')
nyc_path = app.get_asset_url('images/Flag_of_New_York_City.png')

borough_images = {
    "Manhattan": app.get_asset_url('images/boroughs/Manhaton.jpg'),
    "Brooklyn": app.get_asset_url('images/boroughs/Brooklyn.jpg'),
    "Queens": app.get_asset_url('images/boroughs/Queens.jpg'),
    "Bronx": app.get_asset_url('images/boroughs/Bronx.jpg'),
    "Staten Island": app.get_asset_url('images/boroughs/Staten_Island.jpg')
}

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

# 定義 borough_ranks 作為全局變量
BOROUGH_RANKS = {
    "Brooklyn": {"investment_rank": 5, "crime_rank": 1},
    "Manhattan": {"investment_rank": 1, "crime_rank": 4},
    "Queens": {"investment_rank": 2, "crime_rank": 3},
    "Bronx": {"investment_rank": 4, "crime_rank": 2},
    "Staten Island": {"investment_rank": 3, "crime_rank": 5}
}

app.layout = html.Div([
    # 主容器
    html.Div([
        # 第一行：標題和總覽資訊
        html.Div([
            # 左側：標題和 logo
            html.Div([
                html.Img(
                    src=logo_path,
                    style={"height": "40px"}
                ),
                html.Img(
                    src=nyc_path,
                    style={"height": "40px"}
                ),
                html.H1("Airbnb Investor’s Gold Rush: NYC", style={
                    "color": "gray",
                    "margin": "0",
                    "fontSize": "24px"
                })
            ], style={
                "display": "flex",
                "alignItems": "center",
                "gap": "15px",
                "Width": "35%"
            }),
            
            # 總覽資訊
            html.Div([
                html.Div([
                    html.P([
                        "Welcome, future host! ",
                        html.Br(),
                        "Click on one or more boroughs on the map to explore Airbnb business and investment insights.",
                        html.Br(),
                        "Hover over the map or charts for detailed insights.Compare boroughs side by side and make confident, data-driven investment decisions!"

                    ],style={
                            "fontSize": "19px",
                            "color": "gray",
                            "lineHeight":"1.3",
                            "margin": "0"
                        })
                 ], style={
                            "flex": "1",
                            "backgroundColor":"white",
                            "padding": "15px",
                            "borderRadius":"8px",
                            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                            "marginLeft":"100px",
                            "width":"87%"
                        })       
            ])
        ], style={
            "display": "flex",
            "marginBottom": "20px"
        }),

        # 第二行：地圖、選擇區域和詳細資訊
        html.Div([
            # 左側：地圖
            html.Div([
                html.H3("Click Dots to see Borough details", style={
                    "color": "darkred",
                    "textAlign": "center",
                    "marginBottom": "10px",
                    "fontSize": "23px"
                }),
                dcc.Graph(
                    id='nyc-map',
                    figure=create_map_figure(),
                    config={"displayModeBar": False},
                    style={
                        "height": "400px",
                        "width": "100%"
                    }
                )
            ], style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                "width": "32%"
            }),

            # 中間：選擇的區域列表
            html.Div([
                html.H3("Selected Boroughs", style={
                    "color": "gray",
                    "textAlign": "center",
                    "marginBottom": "10px",
                    "fontSize": "18px"
                }),
                html.Div(id="selected-boroughs", style={
                    "backgroundColor": "white",
                    "padding": "10px",
                    "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "borderRadius": "10px",
                    "height": "400px",
                    "overflowY": "auto",
                    "fixe": 1
                }),
                dcc.Store(id='selected-boroughs-store', data=[])
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "minWidth":"300px",
                "marginLeft": "2%"
            }),

            # 右側：詳細資訊
            html.Div(id="borough-details", style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                "flex": "1",
                "marginLeft": "2%",
                "width":"39%",
                "minWidth":"500px",

            })
        ], style={
            "display": "flex",
            "marginBottom": "20px"
        }),

        # 第三行：Potential和Crime圖表
        html.Div([
            html.Div([
                dcc.Graph(
                    figure=create_potential_figure(),
                    config={"displayModeBar": False},
                    style={"height": "450px"}
                )
            ], style={
                "flex": "1",
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"
            }),
            html.Div([
                dcc.Graph(
                    figure=create_crime_figure(),
                    config={"displayModeBar": False},
                    style={"height": "450px"}
                )
            ], style={
                "flex": "1",
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                "marginLeft": "20px"
            })
        ], style={
            "display": "flex",
            "marginBottom": "20px"
        }),

        # 第四行：Price和Room Type圖表
        html.Div([
            html.Div([
                dcc.Graph(
                    id='price-graph',
                    figure=create_price_figure(),
                    config={"displayModeBar": False},
                    style={"height": "450px"}
                )
            ], style={
                "flex": "1",
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"
            }),   
            html.Div([
                dcc.Graph(
                    id='room-graph',
                    figure=create_room_figure(),
                    config={"displayModeBar": False},
                    style={"height": "450px"}
                )
            ], style={
                "flex": "1",
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                "marginLeft": "20px"
            })
        ], style={
            "display": "flex"
        })
    ], style={
        "maxWidth": "1800px",
        "margin": "0 auto",
        "padding": "20px"
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
    
    # 根據 investment_rank 排序
    sorted_boroughs = sorted(boroughs, key=lambda x: x['investment_rank'])
    
    return html.Div([
        html.Div([
            html.Div([
                html.Button(
                    "×",
                    id={'type': 'close-button', 'index': b['name']},
                    style={
                        'position': 'absolute',
                        'right': '8px',
                        'top': '50%',
                        'background': 'none',
                        'border': 'none',
                        'fontSize': '14px',
                        'cursor': 'pointer',
                        'color': '#666',
                        'padding':'4px'
                    }
                ),
                html.H4(b['name'], style={
                    'margin': '0 0 10px 0',
                    'color': '#333',
                    'fontSize': '20px'
                }),
                html.P([  
                    "Investment Rank: ", 
                    html.Strong(f"{b['investment_rank']}")
                ], style={
                    'margin': '0',
                    'fontSize': '14px',
                    'color': '#FF4500',
                    'fontWeight': 'bold'
                })
            ], style={
                'position': 'relative',
                'padding': '10px',
                'marginBottom': '10px',
                'borderRadius': '8px',
                'backgroundColor': BOROUGH_COLORS[b['name']],
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)',
                'height':'45px',
                'width': '92%'
            })
        ]) for b in sorted_boroughs
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '3px'
    })

def update_borough_details(selected_borough):
    if not selected_borough:
        return html.Div("Select a borough to see details",
                       style={"textAlign": "center", "color": "gray"})
    
    return html.Div([
        html.H3("Best Investment Borough", 
            style={"fontSize": "28px","textAlign": "left", "color": "#333", "marginBottom": "20px"}),
        html.Div([
            html.P([
                "Total Listings: ",
                html.Strong(f"{selected_borough['listings']:,}")
            ], style={"marginBottom": "10px"}),
            html.P([
                "Tourism Value: ",
                html.Strong(f"${selected_borough['tourism']:,}M")
            ], style={"marginBottom": "10px"}),
            html.P([
                "Crime Rank: ",
                html.Strong(f"{selected_borough['crime_rank']}")
            ], style={"marginBottom": "10px"}),
        ], style={"fontSize": "20px"}),  # 加上逗號
        html.Div([
            html.Img(
                src=borough_images[selected_borough['name']],
                style={
                    "width": "100%",
                    "height": "100%",
                    "objectFit": "cover",
                    "borderRadius": "8px",
                    "maxHeight": "350px"
                }
            )
        ], style={"width": "65%", "overflow": "hidden"})
    ])

@app.callback(
    [Output('selected-boroughs-store', 'data'),
     Output('selected-boroughs', 'children'),
     Output('price-graph', 'figure'),
     Output('room-graph', 'figure'),
     Output('borough-details', 'children')],
    [Input('nyc-map', 'clickData')],
    [State('selected-boroughs-store', 'data')]
)
def update_selected_boroughs(clickData, current_selections):
    best_investment = "Manhattan"
    details_content = html.Div("Select a borough to see details", 
                             style={"textAlign": "center", "color": "gray"})
    
    borough_image_path = "image"


    if clickData is None:
        return (
            current_selections,
            generate_borough_cards(current_selections),
            create_price_figure(),
            create_room_figure(),
            update_borough_details(None)
        )
    
    clicked_borough = clickData['points'][0]['customdata'][0]
    listings_count = clickData['points'][0]['customdata'][1]
    tourism_value = clickData['points'][0]['customdata'][2]
    
    investment_rank = BOROUGH_RANKS[clicked_borough]["investment_rank"]
    crime_rank = BOROUGH_RANKS[clicked_borough]["crime_rank"]
    
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
        selected_ranks = {b['name']: b['investment_rank'] for b in current_selections}
        best_investment = min(selected_ranks.items(), key=lambda x: x[1])[0]
        
        top_borough = next(b for b in current_selections if b['name'] == best_investment)
        details_content = html.Div([
            html.H3("Best Investment Borough", 
                   style={"textAlign": "center", "color": "darkred","fontSize":"23px","marginTop": "5px"}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H4(f"{top_borough['name']}", 
                            style={"color": "#333", "marginTop": "10px","fontSize":"20px"}),
                        html.P([
                            "Total Listings: ",
                            html.Strong(f"{top_borough['listings']:,}")
                        ], style={"marginBottom": "12px", "fontSize": "16px"}),
                        html.P([
                            "Tourism Value: ",
                            html.Strong(f"${top_borough['tourism']:,}M")
                        ], style={"marginBottom": "12px", "fontSize": "16px"}),
                        html.P([
                            "Crime Rank: ",
                            html.Strong(f"{top_borough['crime_rank']}")
                        ], style={"marginBottom": "12px", "fontSize": "16px"}),
                        html.P([
                            "Investment Rank: ",
                            html.Strong(f"{top_borough['investment_rank']}")
                        ], style={"marginBottom": "12px", "fontSize": "16px"})
                    ])
                ], style={"width": "30%"}),
            
                html.Div([
                    html.Img(
                        src=borough_images[top_borough['name']],
                        style={
                            "width": "100%",
                            "height": "300px",
                            "objectFit": "cover",
                            "borderRadius": "8px",
                            "maxHeight": "350px",
                            "display": "block"
                        }
                    )
                ], style={"width": "65%","overflow": "hidden"})
            ], style={
                "display": "flex",
                "alignItems": "flex-start",
                "justifyContent": "space-between"
            })
        ], style={
            "backgroundColor": "white",
            "borderRadius": "10px",
            "padding": "20px"
        })
    
    return (
        current_selections,
        generate_borough_cards(current_selections),
        create_price_figure([b['name'] for b in current_selections]),
        create_room_figure([b['name'] for b in current_selections]),
        details_content
    )

@app.callback(
    [Output('selected-boroughs-store', 'data', allow_duplicate=True),
     Output('selected-boroughs', 'children', allow_duplicate=True),
     Output('price-graph', 'figure', allow_duplicate=True),
     Output('room-graph', 'figure', allow_duplicate=True),
     Output('borough-details', 'children', allow_duplicate=True)],
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
   
   best_investment = "Manhattan"
   details_content = html.Div("Select a borough to see details", 
                            style={"textAlign": "center", "color": "gray"})
   
   if updated_selections:
       selected_ranks = {b['name']: b['investment_rank'] for b in updated_selections}
       best_investment = min(selected_ranks.items(), key=lambda x: x[1])[0]
       
       top_borough = next(b for b in updated_selections if b['name'] == best_investment)
       details_content = html.Div([
           html.H3("Best Investment Borough", 
                  style={"textAlign": "center", "color": "darkred","fontSize":"23px","marginTop": "5px"}),
           html.Div([
               html.Div([
                   html.Div([
                       html.H4(f"{top_borough['name']}", 
                           style={"color": "#333", "marginTop": "10px","fontSize":"20px"}),
                       html.P([
                           "Total Listings: ",
                           html.Strong(f"{top_borough['listings']:,}")
                       ], style={"marginBottom": "12px", "fontSize": "16px"}),
                       html.P([
                           "Tourism Value: ",
                           html.Strong(f"${top_borough['tourism']:,}M")
                       ], style={"marginBottom": "12px", "fontSize": "16px"}),
                       html.P([
                           "Crime Rank: ",
                           html.Strong(f"{top_borough['crime_rank']}")
                       ], style={"marginBottom": "12px", "fontSize": "16px"}),
                       html.P([
                           "Investment Rank: ",
                           html.Strong(f"{top_borough['investment_rank']}")
                       ], style={"marginBottom": "12px", "fontSize": "16px"})
                   ])
               ], style={"width": "30%"}),
           
               html.Div([
                   html.Img(
                       src=borough_images[top_borough['name']],
                       style={
                           "width": "100%",
                           "height": "300px",
                           "objectFit": "cover",
                           "borderRadius": "8px"
                       }
                   )
               ], style={"width": "65%"})
           ], style={
               "display": "flex",
               "alignItems": "flex-start",
               "justifyContent": "space-between"
           })
       ], style={
           "backgroundColor": "white",
           "borderRadius": "10px",
           "padding": "20px"
       })
   
   return (
       updated_selections,
       generate_borough_cards(updated_selections),
       create_price_figure(selected_borough_names),
       create_room_figure(selected_borough_names),
       details_content
   )


if __name__ == '__main__':
    app.run(debug=False)
        
