# run.py
from app_instance import app
import callbacks  # registers all callbacks

from dash import html, dcc

# Create a wrapper layout that supports routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.title = "Height Predictor"

if __name__ == '__main__':
    app.run(debug=True)
