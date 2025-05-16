import pandas as pd
from sklearn.linear_model import LinearRegression

# Adjust path if needed; this assumes you run from this folder
df = pd.read_csv('../data/height_weight.csv')

model = LinearRegression()
model.fit(df[['Weight (kg)']], df['Height (m)'])

def predict_height(weight_kg):
    return model.predict([[weight_kg]])[0]
