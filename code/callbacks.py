# callbacks.py

from dash import Input, Output, State, callback_context, no_update
from app_instance import app
from data_model import df, model, predict_height
from utils import convert_units, log_prediction, format_table_data
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import urllib.parse

from layout import (
    home_page, dashboard_page, analytics_page,
    LINK_STYLE, ACTIVE_STYLE
)

# --- Navigation highlighting callback ---
@app.callback(
    Output('home-link',      'style'),
    Output('dashboard-link', 'style'),
    Output('analytics-link', 'style'),
    Input('url', 'pathname')
)
def highlight_nav(pathname):
    home_style      = LINK_STYLE.copy()
    dashboard_style = LINK_STYLE.copy()
    analytics_style = LINK_STYLE.copy()
    if pathname == '/':
        home_style.update(ACTIVE_STYLE)
    elif pathname == '/dashboard':
        dashboard_style.update(ACTIVE_STYLE)
    elif pathname == '/analytics':
        analytics_style.update(ACTIVE_STYLE)
    return home_style, dashboard_style, analytics_style


# --- Unified scatter-+-prediction callback ---
@app.callback(
    Output('scatter-plot',           'figure'),
    Output('prediction-output',      'children'),
    Output('session-history',        'data'),
    Input('predict-button',          'n_clicks'),
    Input('unit-selector',           'value'),
    State('input-weight',            'value'),
    State('session-history',         'data')
)
def update_all(n_clicks, units, input_weight, history):
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None
    history = history or []

    # Prepare base data and labels
    if units == 'metric':
        sx, sy = df['Weight (kg)'], df['Height (m)']
        xlab, ylab = 'Weight (kg)', 'Height (m)'
        xr = np.linspace(sx.min(), sx.max(), 100)
    else:
        sx = df['Weight (kg)'] * 2.20462
        sy = df['Height (m)']  * 3.28084
        xlab, ylab = 'Weight (lbs)', 'Height (ft)'
        xr = np.linspace(df['Weight (kg)'].min(), df['Weight (kg)'].max(), 100)

    # Build scatter + regression line
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sx, y=sy, mode='markers', name='Data', marker=dict(color='blue')
    ))
    yp = model.predict(xr.reshape(-1,1))
    xl, yl = convert_units(xr, yp, to=units)
    fig.add_trace(go.Scatter(
        x=xl, y=yl, mode='lines', name='Regression', line=dict(color='black')
    ))

    display_string = ''

    # Handle prediction click
    if triggered == 'predict-button.n_clicks' and input_weight is not None:
        # 1) convert input to kilograms for the model
        weight_kg = input_weight if units == 'metric' else input_weight * 0.453592
        # 2) predict height in metres
        height_m = predict_height(weight_kg)
        # 3) convert both for display
        disp_w, disp_h = convert_units(weight_kg, height_m, to=units)
        unit_lbl = 'm' if units == 'metric' else 'ft'

        # 4) plot the prediction point
        fig.add_trace(go.Scatter(
            x=[disp_w], y=[disp_h], mode='markers+text', name='Prediction',
            marker=dict(color='red', size=10),
            text=[f'{disp_h:.2f} {unit_lbl}'], textposition='top center'
        ))

        # 5) prepare the display string
        display_string = f'Predicted height: {disp_h:.2f} {unit_lbl}'

        # 6) log the prediction (weight in kg, height in m, units)
        log_prediction(weight_kg, height_m, units)

        # 7) append to session history
        history.append({
            'input_weight_metric':  weight_kg,
            'predicted_height_m':   height_m,
            'datetime':             datetime.now().isoformat()
        })

    # Final layout settings
    fig.update_layout(
        title='Height vs Weight',
        xaxis_title=xlab,
        yaxis_title=ylab,
        font_family='Arial, sans-serif'
    )

    return fig, display_string, history


# --- History Table callback ---
@app.callback(
    Output('history-table', 'data'),
    Input('unit-selector', 'value'),
    Input('session-history',  'data')
)
def update_table(units, history):
    if not history:
        return []
    return format_table_data(history, units)


# --- Page routing callback ---
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return home_page
    elif pathname == '/dashboard':
        return dashboard_page
    elif pathname == '/analytics':
        return analytics_page
    else:
        return home_page


# --- Export email callback ---
@app.callback(
    Output('export-email', 'href'),
    Output('export-email', 'children'),
    Input('history-table',    'data'),
    Input('history-table',    'selected_rows')
)
def make_mailto(table_data, selected_rows):
    if not table_data:
        return '', 'Email My History'
    rows = table_data if not selected_rows else [table_data[i] for i in selected_rows]
    header = ["Weight", "Predicted Height", "Time"]
    lines = ["\t".join(header)]
    for r in rows:
        lines.append("\t".join([r['input_weight'], r['predicted_height'], r['datetime']]))
    body = "\n".join(lines)
    subject = "Your Height Predictions"
    href = (
        f"mailto:?subject={urllib.parse.quote(subject)}"
        f"&body={urllib.parse.quote(body)}"
    )
    return href, 'Email My History'


# --- Persist unit selection in Store ---
@app.callback(
    Output('unit-store', 'data'),
    Input('unit-selector', 'value')
)
def save_unit(units):
    return units


# --- Dynamic Histograms callback ---
@app.callback(
    Output('weight-histogram', 'figure'),
    Output('height-histogram','figure'),
    Input('unit-store',    'data')
)
def update_histograms(units):
    if units == 'metric':
        w, wl = df['Weight (kg)'], 'Weight (kg)'
        h, hl = df['Height (m)'],    'Height (m)'
    else:
        w, wl = df['Weight (kg)'] * 2.20462, 'Weight (lbs)'
        h, hl = df['Height (m)']  * 3.28084, 'Height (ft)'

    fig_w = go.Figure(go.Histogram(x=w))
    fig_w.update_layout(
        title='Distribution of Weights',
        xaxis_title=wl, yaxis_title='Count',
        font_family='Arial, sans-serif'
    )

    fig_h = go.Figure(go.Histogram(x=h))
    fig_h.update_layout(
        title='Distribution of Heights',
        xaxis_title=hl, yaxis_title='Count',
        font_family='Arial, sans-serif'
    )

    return fig_w, fig_h