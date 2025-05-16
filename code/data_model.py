import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('../data/height_weight.csv')

model = LinearRegression()
model.fit(df[['Weight (kg)']], df['Height (m)'])

def predict_height(df, model, weight):
    return model.predict([[weight]])[0]