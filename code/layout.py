from dash import html, dcc
import dash.dash_table

# Style for the nav links
nav_link_style = {
    'padding': '8px 12px',
    'backgroundColor': '#0074D9',
    'color': 'white',
    'borderRadius': '4px',
    'textDecoration': 'none',
    'marginRight': '10px'
}

# --- Home page layout ---
home_layout = html.Div([
    html.H1("Height Predictor Application", style={'marginTop': '100px'}),
    html.P(
        "This application allows you to predict height from weight using a linear regression model. "
        "Switch to the dashboard using the navigation above to input your weight, see predictions, and view your history.",
        style={
            'fontSize': '18px',
            'maxWidth': '600px',
            'margin': 'auto',
            'textAlign': 'center'
        }
    ),
], style={'textAlign': 'center'})

# --- Dashboard page layout ---
dashboard_layout = html.Div([
    html.H2("Height vs Weight Predictor", style={'marginBottom': '20px'}),
    dcc.Dropdown(
        id='unit-selector',
        options=[
            {'label': 'Metric (kg, m)',   'value': 'metric'},
            {'label': 'Imperial (lbs, ft)', 'value': 'imperial'}
        ],
        value='metric',
        clearable=False,
        style={'width': '250px', 'marginBottom': '20px'}
    ),
    html.Div([
        html.Div(
            dcc.Graph(id='scatter-plot'),
            style={'flex': '2', 'paddingRight': '20px'}
        ),
        html.Div([
            html.H4("Your Recent Predictions", style={'marginBottom': '10px'}),
            dash.dash_table.DataTable(
                id='history-table',
                columns=[
                    {'name': 'Weight',           'id': 'input_weight'},
                    {'name': 'Predicted Height', 'id': 'predicted_height'},
                    {'name': 'Time',             'id': 'datetime'}
                ],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '8px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f1f1f1'},
                page_action='none'
            )
        ], style={
            'flex': '1',
            'backgroundColor': '#f9f9f9',
            'padding': '15px',
            'border': '1px solid #ddd',
            'borderRadius': '6px'
        })
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'flex-start',
        'marginBottom': '30px'
    }),
    dcc.Store(id='stored-prediction'),
    dcc.Store(id='session-history'),
    html.Div([
        html.Label(id='weight-label', style={'fontWeight': 'bold', 'marginBottom': '8px'}),
        dcc.Input(
            id='input-weight',
            type='number',
            min=30,
            max=350,
            step=0.1,
            style={'width': '150px', 'padding': '8px', 'marginRight': '10px'}
        ),
        html.Button(
            "Predict Height",
            id='predict-button',
            n_clicks=0,
            style={
                'padding': '8px 12px',
                'backgroundColor': '#0074D9',
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'cursor': 'pointer'
            }
        )
    ], style={'margin': '30px 0'}),
    html.Div(id='prediction-output', style={
        'fontSize': '18px',
        'padding': '10px',
        'backgroundColor': '#f4f4f4',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'width': 'fit-content',
        'marginBottom': '20px'
    })
], style={
    'fontFamily': 'Arial, sans-serif',
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

# --- Root layout with navigation ---
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link("Home",      href='/',          style=nav_link_style),
        dcc.Link("Dashboard", href='/dashboard', style=nav_link_style),
    ], style={
        'position': 'fixed',
        'top': '10px',
        'left': '10px',
        'zIndex': 100
    }),
    html.Div(id='page-content', style={'marginTop': '60px'})
])
