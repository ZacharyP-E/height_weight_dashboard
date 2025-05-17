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

@app.callback(
    Output('weight-label', 'children'),
    Input('unit-selector', 'value')
)
def update_weight_label(units):
    return f"Enter your weight ({'kg' if units=='metric' else 'lbs'}):"


@app.callback(
    Output('scatter-plot', 'figure'),
    Output('prediction-output', 'children'),
    Output('stored-prediction', 'data'),
    Output('session-history', 'data'),
    Input('predict-button', 'n_clicks'),
    Input('unit-selector', 'value'),
    State('input-weight', 'value'),
    State('stored-prediction', 'data'),
    State('session-history', 'data')
)
def update_all(n_clicks, units, input_weight, stored, history):
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    history = history or []
    display_string = no_update
    store_update = no_update

    # Base data & labels
    if units == 'metric':
        sx = df['Weight (kg)']
        sy = df['Height (m)']
        xlab, ylab = "Weight (kg)", "Height (m)"
        xr = np.linspace(sx.min(), sx.max(), 100)
    else:
        sx = df['Weight (kg)'] * 2.20462
        sy = df['Height (m)'] * 3.28084
        xlab, ylab = "Weight (lbs)", "Height (ft)"
        xr = np.linspace(df['Weight (kg)'].min(),
                         df['Weight (kg)'].max(), 100)

    # Build scatter + regression
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sx, y=sy, mode='markers', name='Data', marker=dict(color='blue')
    ))
    fig.update_layout(
        title='Height vs Weight',
        xaxis_title=xlab,
        yaxis_title=ylab,
        font_family='Arial, sans-serif'
    )

    yp = model.predict(xr.reshape(-1, 1))
    xl, yl = convert_units(xr, yp, to=units)
    fig.add_trace(go.Scatter(
        x=xl, y=yl, mode='lines', name='Regression', line=dict(color='black')
    ))

    # Handle predict-button click
    if triggered == 'predict-button.n_clicks' and input_weight is not None:
        # Convert back to metric if needed
        raw_weight = input_weight if units == 'metric' else input_weight / 2.20462
        pred = predict_height(df, model, raw_weight)
        display = pred if units == 'metric' else pred * 3.28084
        unit_label = 'm' if units == 'metric' else 'ft'
        display_string = f'Predicted height: {display:.2f} {unit_label}'

        new_entry = {
            'input_weight': f'{input_weight:.2f}',
            'predicted_height': f'{display:.2f} {unit_label}',
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        log_prediction(new_entry)
        store_update = new_entry
        history.append(new_entry)

    return fig, display_string, store_update, history


@app.callback(
    Output('history-table', 'data'),
    Input('unit-selector', 'value'),
    Input('session-history', 'data')
)
def update_table(units, history):
    if not history:
        return []
    return format_table_data(history, units)


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


@app.callback(
    [
        Output('home-link',      'style'),
        Output('dashboard-link', 'style'),
        Output('analytics-link', 'style'),
    ],
    Input('url', 'pathname')
)
def highlight_nav(pathname):
    home_style = LINK_STYLE.copy()
    dash_style = LINK_STYLE.copy()
    analytics_style = LINK_STYLE.copy()

    if pathname == '/':
        home_style.update(ACTIVE_STYLE)
    elif pathname == '/dashboard':
        dash_style.update(ACTIVE_STYLE)
    elif pathname == '/analytics':
        analytics_style.update(ACTIVE_STYLE)

    return home_style, dash_style, analytics_style


@app.callback(
    Output('export-email', 'href'),
    Output('export-email', 'children'),
    Input('history-table', 'data'),
    Input('history-table', 'selected_rows')
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


# --- Dynamic Histograms callback ---
@app.callback(
    Output('weight-histogram', 'figure'),
    Output('height-histogram', 'figure'),
    Input('unit-store', 'data')
)
def update_histograms(units):
    if units == 'metric':
        w = df['Weight (kg)']; wl = 'Weight (kg)'
        h = df['Height (m)'];    hl = 'Height (m)'
    else:
        w = df['Weight (kg)'] * 2.20462; wl = 'Weight (lbs)'
        h = df['Height (m)']  * 3.28084; hl = 'Height (ft)'

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

@app.callback(
    Output('unit-store', 'data'),
    Input('unit-selector', 'value')
)
def save_unit(units):
    return units