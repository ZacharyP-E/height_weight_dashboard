# layout.py

from dash import html, dcc
import dash.dash_table
import plotly.express as px
import plotly.graph_objects as go
from data_model import df  # your DataFrame loaded in data_mode.py
import numpy as np

# --- Navbar styles ---
NAV_STYLE = {
    'display': 'flex',
    'backgroundColor': '#0074D9',
    'padding': '10px',
    'alignItems': 'center'
}
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
        html.Li([html.Strong("Unit Selector:"),    " Toggle between kg/m and lbs/ft."]),
        html.Li([html.Strong("Interactive Plot:"), " See your point on the regression line."]),
        html.Li([html.Strong("History Table:"),    " Review your last five predictions."]),
        html.Li([html.Strong("Row Selection:"),    " Select rows to export."]),
        html.Li([html.Strong("Email Export:"),     " Email all or selected rows."]),
        html.Li([html.Strong("Analytics Page:"),   " View weight & height histograms."])
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
                style_table={'overflowX': 'auto', 'fontFamily': 'Arial, sans-serif'},
                style_cell={'textAlign': 'center', 'padding': '8px', 'fontFamily': 'Arial, sans-serif'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f1f1f1', 'fontFamily': 'Arial, sans-serif'},
                page_action='none'
            ),
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

    dcc.Store(id='stored-prediction'),
    dcc.Store(id='session-history'),

    html.Div([
        html.Label(id='weight-label', style={'fontWeight': 'bold', 'marginBottom': '8px'}),
        dcc.Input(id='input-weight', type='number', min=30, max=350, step=0.1,
                  style={'width': '150px', 'padding': '8px', 'marginRight': '10px'}),
        html.Button("Predict Height", id='predict-button', n_clicks=0,
                    style={'padding': '8px 12px','backgroundColor': '#0074D9','color': 'white',
                           'border': 'none','borderRadius': '4px','cursor': 'pointer'})
    ], style={'margin': '30px 0'}),

    html.Div(id='prediction-output', style={
        'fontSize': '18px',
        'padding': '10px',
        'backgroundColor': '#f4f4f4',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'width': 'fit-content',
        'marginBottom': '20px'
    }),

    html.A(
        html.Button("📧 Email My History", style={
            'padding': '10px 16px',
            'fontSize': '14px',
            'backgroundColor': 'white',
            'color': '#0074D9',
            'border': '2px solid #0074D9',
            'borderRadius': '4px',
            'cursor': 'pointer'
        }),
        id='export-email',
        href='',
        target='_blank',
        style={'position': 'fixed', 'bottom': '20px', 'right': '20px', 'zIndex': 1000}
    )

], style={
    'fontFamily': 'Arial, sans-serif',
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

# --- Analytics Page: two histograms side by side ---
# --- Compute stats ---
w = df['Weight (kg)']
h = df['Height (m)']

mean_w, med_w, std_w = w.mean(), w.median(), w.std()
mean_h, med_h, std_h = h.mean(), h.median(), h.std()

# --- Weight histogram bins & colors ---
counts_w, bins_w = np.histogram(w, bins=30)
centers_w = (bins_w[:-1] + bins_w[1:]) / 2

colors_w = []
for x in centers_w:
    d = abs(x - mean_w)
    if d <= std_w:
        colors_w.append('rgba(0,128,0,0.6)')    # ±1σ
    elif d <= 2*std_w:
        colors_w.append('rgba(0,128,0,0.3)')    # ±2σ
    else:
        colors_w.append('lightgrey')            # beyond

hist_w = go.Figure()
hist_w.add_trace(go.Bar(
    x=centers_w, y=counts_w,
    marker_color=colors_w,
    name='Weight'
))
hist_w.add_vline(x=mean_w, line=dict(color='red', dash='dash'),
                 annotation_text='Mean', annotation_position='top right')
hist_w.add_vline(x=med_w,  line=dict(color='blue', dash='dot'),
                 annotation_text='Median', annotation_position='top left')
hist_w.update_layout(
    title='Weight Distribution',
    xaxis_title='Weight (kg)',
    yaxis_title='Count',
    font_family='Arial, sans-serif'
)

# --- Height histogram bins & red shading for σ-bands ---
counts_h, bins_h = np.histogram(h, bins=30)
centers_h = (bins_h[:-1] + bins_h[1:]) / 2

colors_h = []
for x in centers_h:
    d = abs(x - mean_h)
    if d <= std_h:
        # within ±1σ → darker red
        colors_h.append('rgba(255, 0, 0, 0.6)')
    elif d <= 2*std_h:
        # between 1σ and 2σ → lighter red
        colors_h.append('rgba(255, 0, 0, 0.3)')
    else:
        # beyond 2σ → grey
        colors_h.append('lightgrey')

hist_h = go.Figure()
hist_h.add_trace(go.Bar(
    x=centers_h,
    y=counts_h,
    marker_color=colors_h,
    name='Height'
))
hist_h.add_vline(x=mean_h,
                 line=dict(color='red', dash='dash'),
                 annotation_text='Mean',
                 annotation_position='top right')
hist_h.add_vline(x=med_h,
                 line=dict(color='blue', dash='dot'),
                 annotation_text='Median',
                 annotation_position='top left')
hist_h.update_layout(
    title='Height Distribution',
    xaxis_title='Height (m)',
    yaxis_title='Count',
    font_family='Arial, sans-serif'
)


analytics_page = html.Div([
    html.H2("Data Distributions", style={'marginBottom': '20px'}),
    html.Div([
        html.Div(dcc.Graph(figure=hist_w), style={'flex': '1', 'paddingRight': '10px'}),
        html.Div(dcc.Graph(figure=hist_h), style={'flex': '1', 'paddingLeft': '10px'})
    ], style={'display': 'flex', 'alignItems': 'flex-start'})
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
        dcc.Link('Dashboard', href='/dashboard',  id='dashboard-link', style=LINK_STYLE),
        dcc.Link('Analytics', href='/analytics',  id='analytics-link', style=LINK_STYLE),
    ], style=NAV_STYLE),

    html.Div(id='page-content')
], style={
    'fontFamily': 'Arial, sans-serif'
})
