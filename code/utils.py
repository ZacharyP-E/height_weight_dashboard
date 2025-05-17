import pandas as pd
import os
from datetime import datetime
import getpass

def convert_units(weight_kg, height_m, to='metric'):
    if to == 'imperial':
        return weight_kg * 2.20462, height_m * 3.28084
    return weight_kg, height_m

def log_prediction(weight, height, units,
                   path='../data/prediction_log.csv'):
    user = getpass.getuser()
    entry = pd.DataFrame([{
        'datetime': datetime.now().isoformat(),
        'username': user,
        'input_weight': weight,
        'predicted_height': height,
        'input_units': units
    }])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    entry.to_csv(path, mode='a', index=False,
                 header=not os.path.exists(path))

def format_table_data(history, units):
    rows = []
    for r in history:
        w, h = convert_units(r['input_weight_metric'],
                             r['predicted_height_m'],
                             to=units)
        rows.append({
            'selected':          False,
            'input_weight':      f"{w:.1f} {'kg' if units=='metric' else 'lbs'}",
            'predicted_height': f"{h:.2f} {'m'  if units=='metric' else 'ft'}",
            'datetime':          r['datetime']
        })
    return rows
