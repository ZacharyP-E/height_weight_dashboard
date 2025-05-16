from dash import Input, Output, State, callback_context, no_update
from app_instance import app
from data_model import df, model, predict_height
from utils import convert_units, log_prediction, format_table_data
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from layout import home_page, dashboard_page, LINK_STYLE, ACTIVE_STYLE


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

    # Build figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sx, y=sy,
                             mode='markers',
                             name='Data',
                             marker=dict(color='blue')))
    fig.update_layout(title='Height vs Weight')

    # Regression
    yp = model.predict(xr.reshape(-1,1))
    xl, yl = convert_units(xr, yp, to=units)
    fig.add_trace(go.Scatter(x=xl, y=yl,
                             mode='lines',
                             name='Regression',
                             line=dict(color='black')))

    # Predict?
    if triggered=='predict-button.n_clicks' and input_weight is not None:
        wg = (input_weight if units=='metric'
              else input_weight*0.453592)
        hm = predict_height(wg)
        dw, dh = convert_units(wg, hm, to=units)
        suf = 'm' if units=='metric' else 'ft'

        fig.add_trace(go.Scatter(
            x=[dw], y=[dh],
            mode='markers+text',
            name='Prediction',
            marker=dict(color='red', size=10),
            text=["Your predicted height"],
            textposition="top center"
        ))

        display_string = f"Predicted height: {dh:.2f} {suf}"
        store_update = {'input_weight_metric': wg,
                        'predicted_height_m': hm}

        new_row = {
            'datetime': datetime.now().strftime("%H:%M:%S"),
            'input_weight_metric': wg,
            'predicted_height_m': hm
        }
        history = [new_row] + history[:4]

        log_prediction(weight=input_weight,
                       height=dh,
                       units=units)

    # Unit-change after prediction?
    elif triggered=='unit-selector.value' and stored:
        wg = stored['input_weight_metric']
        hm = stored['predicted_height_m']
        dw, dh = convert_units(wg, hm, to=units)
        suf = 'm' if units=='metric' else 'ft'

        fig.add_trace(go.Scatter(
            x=[dw], y=[dh],
            mode='markers+text',
            name='Prediction',
            marker=dict(color='red', size=10),
            text=["Your predicted height"],
            textposition="top center"
        ))

        display_string = f"Predicted height: {dh:.2f} {suf}"

    fig.update_layout(xaxis_title=xlab, yaxis_title=ylab)
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
    if pathname == '/dashboard':
        return dashboard_page
    return home_page

@app.callback(
    [Output('home-link',      'style'),
     Output('dashboard-link', 'style')],
    Input('url', 'pathname')
)
def update_nav_styles(pathname):
    home_style      = LINK_STYLE.copy()
    dashboard_style = LINK_STYLE.copy()

    if pathname in ['/', '']:
        home_style.update(ACTIVE_STYLE)
    elif pathname == '/dashboard':
        dashboard_style.update(ACTIVE_STYLE)

    return home_style, dashboard_style
