from app_instance import app
from layout import layout
import callbacks

app.title = "Height Predictor"
app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)