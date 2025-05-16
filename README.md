# Height vs Weight Predictor

A Dash app that predicts height from weight using linear regression, with metric/imperial units, interactive plot, and history table.

```
├── app_instance.py # creates Dash app
├── layout.py # defines pages & navbar
├── callbacks.py # registers callbacks
├── data_mode.py # loads data & trains model
├── utils.py # helpers (conversion, logging)
├── run.py # entry point
├── data/
│ └── height_weight.csv # dataset
└── README.md # you are here
```




## Setup

```bash
python run.py
Open http://127.0.0.1:8050/ in your browser.
```

## Usage

1. Switch between Home and Dashboard via the navbar.
2. On Dashboard, select units, enter weight, and click Predict Height.
3. See your point on the plot and recent history in the table.

## Data & Logs

data/height_weight.csv — training dataset
data/prediction_log.csv — appended user predictions