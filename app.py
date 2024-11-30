import dash
from dash import dcc, html
from fig_map import create_map_figure
from fig_price import create_price_figure
from fig_crime import create_crime_figure
from fig_potential import create_potential_figure
from fig_room import create_room_figure

app = dash.Dash(__name__)

app.layout = html.Div([
    # 主容器
    html.Div([
        # 第一列：potential 和 crime
        html.Div([
            # 左側：觀光潛力分析
            html.Div([
                dcc.Graph(
                    figure=create_potential_figure(),
                    config={'displayModeBar': False}
                )
            ], className='column', style={'width': '50%', 'display': 'inline-block'}),
            
            # 右側：犯罪分析
            html.Div([
                dcc.Graph(
                    figure=create_crime_figure(),
                    config={'displayModeBar': False}
                )
            ], className='column', style={'width': '50%', 'display': 'inline-block'})
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'marginBottom': '20px'
        }),
        
        # 第二列：地圖 (置中)
        html.Div([
            html.Div([
                dcc.Graph(
                    figure=create_map_figure(),
                    config={'displayModeBar': False}
                )
            ], className='column', style={'width': '60%', 'margin': '0 auto'})
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'marginBottom': '20px'
        }),
        
        # 第三列：price 和 room type
        html.Div([
            # 左側：價格分析
            html.Div([
                dcc.Graph(
                    figure=create_price_figure(),
                    config={'displayModeBar': False}
                )
            ], className='column', style={'width': '50%', 'display': 'inline-block'}),
            
            # 右側：房型分析
            html.Div([
                dcc.Graph(
                    figure=create_room_figure(),
                    config={'displayModeBar': False}
                )
            ], className='column', style={'width': '50%', 'display': 'inline-block'})
        ], style={
            'display': 'flex',
            'justifyContent': 'center'
        })
    ], style={
        'width': '100%',
        'maxWidth': '1800px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': 'white',
        'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
        'borderRadius': '10px'
    })
], style={
    'padding': '20px',
    'backgroundColor': '#f5f5f5',
    'minHeight': '100vh'
})

# 添加自定義 CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NYC Airbnb Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            .column {
                padding: 10px;
            }
            .js-plotly-plot .plotly .modebar {
                display: none !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)