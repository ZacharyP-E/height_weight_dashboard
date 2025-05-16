import pandas as pd
import numpy as np
import os

# Ensure output directory exists
os.makedirs('../data', exist_ok=True)

# Generate synthetic data
np.random.seed(42)
weights = np.random.normal(loc=70, scale=10, size=100)
heights = 1.5 + 0.01 * weights + np.random.normal(0, 0.05, size=100)

df = pd.DataFrame({
    'Weight (kg)': weights,
    'Height (m)': heights
})

# Save to CSV
df.to_csv('../data/height_weight.csv', index=False)

print("Data saved to ../data/height_weight.csv")
