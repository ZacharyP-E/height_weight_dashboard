# layout.py

from dash import html, dcc
import dash.dash_table

# --- Navbar styles ---
NAV_STYLE = {
    'display': 'flex',
    'backgroundColor': '#0074D9',
    'padding': '10px',
    'alignItems': 'center'
}

# white buttons with blue text
LINK_STYLE = {
    'backgroundColor': 'white',
    'color': '#0074D9',
    'marginRight': '10px',
    'padding': '8px 16px',
    'borderRadius': '4px',
    'textDecoration': 'none',
    'fontWeight': 'bold',
    'transition': 'all 0.2s ease'
}

# active link: slightly larger & bolder
ACTIVE_STYLE = {
    'fontSize': '18px',
    'padding': '10px 18px',
    'boxShadow': '0 2px 6px rgba(0,0,0,0.2)'
}

# --- Title / Instruction Page ---
home_page = html.Div([
    html.H1("Height vs Weight Predictor", style={'marginBottom': '10px'}),
    html.P(
        "Predict your height from your weight using a linear regression model. "
        "Switch between metric and imperial units, make interactive predictions, "
        "and keep track of your last five guesses.",
        style={'maxWidth': '600px', 'lineHeight': '1.5', 'margin': '0 auto'}
    ),

    html.H4("Key Features:", style={'marginTop': '30px'}),
    html.Ul([
        html.Li([ html.Strong("Unit Selector:"), " Toggle between kg/m and lbs/ft." ]),
        html.Li([ html.Strong("Interactive Plot:"), " See your point on the regression line." ]),
        html.Li([ html.Strong("History Table:"), " Review your last five predictions." ]),
        html.Li([ html.Strong("Row Selection:"), " Check boxes to pick any entries." ]),
        html.Li([ html.Strong("Email Export:"), " Send all or only selected rows via your mail client." ]),
        html.Li([ html.Strong("Multi-Page Layout:"), " Navigate between Home and Dashboard easily." ])
    ], style={'maxWidth': '600px', 'margin': '0 auto', 'textAlign': 'left'}),

    dcc.Link(
        html.Button(
            "Go to Dashboard",
            style={
                'padding': '12px 24px',
                'fontSize': '16px',
                'marginTop': '20px',
                'backgroundColor': '#0074D9',
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'cursor': 'pointer'
            }
        ),
        href='/dashboard'
    )
], style={
    'fontFamily': 'Arial, sans-serif',
    'textAlign': 'center',
    'padding': '50px'
})

# --- Main Dashboard Page ---
dashboard_page = html.Div([

    html.H2("Height vs Weight Predictor", style={'marginBottom': '20px'}),

    dcc.Dropdown(
        id='unit-selector',
        options=[
            {'label': 'Metric (kg, m)',     'value': 'metric'},
            {'label': 'Imperial (lbs, ft)', 'value': 'imperial'}
        ],
        value='metric',
        clearable=False,
        style={'width': '250px', 'marginBottom': '20px'}
    ),

    # Flex container for chart and table
    html.Div([
        html.Div(
            dcc.Graph(id='scatter-plot'),
            style={'flex': '2'}
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
                data=[],                  
                row_selectable='multi',   
                selected_rows=[],         
                style_table={
                    'overflowX': 'auto',
                    'fontFamily': 'Arial, sans-serif'   # ensure outer table uses same font
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                    'fontFamily': 'Arial, sans-serif'   # set cell font
                },
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#f1f1f1',
                    'fontFamily': 'Arial, sans-serif'   # set header font
                },
                page_action='none'
            ),

            # Export scope selector
            dcc.RadioItems(
                id='export-option',
                options=[
                    {'label': 'All',      'value': 'all'},
                    {'label': 'Selected', 'value': 'selected'}
                ],
                value='all',
                inline=True,
                style={'marginTop': '10px'}
            ),

        ], style={
            'flex': '1',
            'marginLeft': '20px',
            'backgroundColor': '#f9f9f9',
            'padding': '15px',
            'border': '1px solid #ddd',
            'borderRadius': '6px'
        }),

    ], style={
        'display': 'flex',
        'alignItems': 'flex-start',
        'marginBottom': '20px'
    }),

    # Stores for callbacks
    dcc.Store(id='stored-prediction'),
    dcc.Store(id='session-history'),

    # Input controls
    html.Div([
        html.Label(
            id='weight-label',
            style={'fontWeight': 'bold', 'marginBottom': '8px'}
        ),
        dcc.Input(
            id='input-weight',
            type='number',
            min=30, max=350, step=0.1,
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

    # Prediction output
    html.Div(
        id='prediction-output',
        style={
            'fontSize': '18px',
            'padding': '10px',
            'backgroundColor': '#f4f4f4',
            'border': '1px solid #ddd',
            'borderRadius': '5px',
            'width': 'fit-content',
            'marginBottom': '20px'
        }
    ),

    # Export via email button
    html.A(
        html.Button(
            "📧 Email My History",
            style={
                'padding': '10px 16px',
                'fontSize': '14px',
                'backgroundColor': 'white',
                'color': '#0074D9',
                'border': '2px solid #0074D9',
                'borderRadius': '4px',
                'cursor': 'pointer'
            }
        ),
        id='export-email',
        href='',          
        target='_blank',
        style={
            'position': 'fixed',
            'bottom': '20px',
            'right': '20px',
            'zIndex': 1000
        }
    )

], style={
    'fontFamily': 'Arial, sans-serif',
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

# --- Top‐level layout with URL routing and navbar ---
layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Nav([
        dcc.Link('Home',      href='/',           id='home-link',      style=LINK_STYLE),
        dcc.Link('Dashboard', href='/dashboard',  id='dashboard-link', style=LINK_STYLE)
    ], style=NAV_STYLE),

    html.Div(id='page-content')
], style={
    'fontFamily': 'Arial, sans-serif'
})
