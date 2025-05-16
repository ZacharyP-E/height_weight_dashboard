from dash import Input, Output, State, callback_context, no_update
from app_instance import app
from layout import home_layout, dashboard_layout
from data_model import df, model, predict_height
from utils import convert_units, log_prediction, format_table_data
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

# --- Page router callback ---
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_layout
    return home_layout

# --- Unified update callback (graph, prediction, history) ---
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
    triggered = ctx.triggered and ctx.triggered[0]['prop_id']

    history = history or []
    display_str = no_update
    store = no_update

    # Prepare base data
    if units == 'metric':
        sx = df['Weight (kg)']
        sy = df['Height (m)']
        xlab, ylab = "Weight (kg)", "Height (m)"
        xr = np.linspace(sx.min(), sx.max(), 100)
    else:
        sx = df['Weight (kg)'] * 2.20462
        sy = df['Height (m)']   * 3.28084
        xlab, ylab = "Weight (lbs)", "Height (ft)"
        xr = np.linspace(df['Weight (kg)'].min(), df['Weight (kg)'].max(), 100)

    # Build figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sx, y=sy, mode='markers',
                             name='Data', marker=dict(color='blue')))
    fig.update_layout(title='Height vs Weight')

    # Regression line
    yp = model.predict(xr.reshape(-1, 1))
    xl, yl = convert_units(xr, yp, to=units)
    fig.add_trace(go.Scatter(x=xl, y=yl, mode='lines',
                             name='Regression', line=dict(color='black')))

    # Case 1: Prediction made
    if triggered == 'predict-button.n_clicks' and input_weight is not None:
        wg = input_weight if units == 'metric' else input_weight * 0.453592
        hm = predict_height(wg)
        dw, dh = convert_units(wg, hm, to=units)
        suf = 'm' if units == 'metric' else 'ft'

        fig.add_trace(go.Scatter(
            x=[dw], y=[dh],
            mode='markers+text',
            name='Prediction',
            marker=dict(color='red', size=10),
            text=["Your predicted height"],
            textposition="top center"
        ))

        display_str = f"Predicted height: {dh:.2f} {suf}"
        store = {'input_weight_metric': wg, 'predicted_height_m': hm}

        # Update session history
        new = {
            'datetime': datetime.now().strftime("%H:%M:%S"),
            'input_weight_metric': wg,
            'predicted_height_m': hm
        }
        history = [new] + history[:4]

        # Log to CSV
        log_prediction(weight=input_weight, height=dh, units=units)

    # Case 2: Unit toggled after a prediction
    elif triggered == 'unit-selector.value' and stored:
        wg = stored['input_weight_metric']
        hm = stored['predicted_height_m']
        dw, dh = convert_units(wg, hm, to=units)
        suf = 'm' if units == 'metric' else 'ft'

        fig.add_trace(go.Scatter(
            x=[dw], y=[dh],
            mode='markers+text',
            name='Prediction',
            marker=dict(color='red', size=10),
            text=["Your predicted height"],
            textposition="top center"
        ))

        display_str = f"Predicted height: {dh:.2f} {suf}"

    fig.update_layout(xaxis_title=xlab, yaxis_title=ylab)
    return fig, display_str, store, history

# --- History table update callback ---
@app.callback(
    Output('history-table', 'data'),
    Input('unit-selector', 'value'),
    Input('session-history', 'data')
)
def update_table(units, history):
    return format_table_data(history, units) if history else []
