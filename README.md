# Height vs Weight Predictor

A Dash app that predicts height from weight using linear regression.  
Features metric/imperial units, an interactive plot, session‐based history with row selection, and an “Email My History” export.

```
├── app_instance.py # creates Dash app
├── layout.py # defines pages & navbar
├── callbacks.py # registers callbacks
├── data_mode.py # loads data & trains model
├── utils.py # helpers (conversion, logging)
├── run.py # entry point
├── requirements.txt # Python dependencies
├── data/
│ └── height_weight.csv # dataset
└── README.md # you are here
```




## Setup

```bash
python run.py
```

Open http://127.0.0.1:8050/ in your browser.

## Usage

1. **Navigate**
   Use the navbar to switch between **Home** and **Dashboard**.

2. **Predict**
   On Dashboard:

   - Select **Metric** or **Imperial**.

   - Enter your weight and click **Predict Height**.

   - View your point on the regression plot and the result panel.

3. **History & Export**
   - Your last 5 predictions appear in the table on the right.
   - **Select rows** via the checkboxes, choose **All** or **Selected**, then click **📧 Email My History**.
   - This opens your mail client with a pre-filled draft of the chosen rows.

## Data & Logs

data/height_weight.csv — training dataset
data/prediction_log.csv — appended user predictions



## Deployment Options

https://community.plotly.com/t/how-to-deploy-dash-app-internally-in-local-network/61312



https://community.plotly.com/t/deploy-on-internal-server-without-git-and-docker/68574



https://www.reddit.com/r/databricks/comments/1fqkdvt/can_you_deploy_a_web_app_in_databricks/



https://github.com/nickjj/docker-flask-example



## Authenticaiton

https://www.reddit.com/r/flask/comments/1kmmfdf/seeking_guidance_on_enterpriselevel_auth_in_flask/



https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login



https://pypi.org/project/Flask-Login/