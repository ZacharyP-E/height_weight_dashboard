from dash import Dash

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder='../assets'   # point to the sibling assets directory
)
