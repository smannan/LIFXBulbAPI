
import json
import math
import numpy as np
import os
import pandas as pd
import pickle

from flask import Flask
from flask import request
from influxdb_client import InfluxDBClient
from keras.models import model_from_json

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
LIFX_filename = '{0}/models/smart_bulb_arima.pkl'.format(dir_path)
PGE_filename = '{0}/models/pge_lstm_model.json'.format(dir_path)
PGE_weights = '{0}/models/pge_lstm_model_weights.h5'.format(dir_path)

bucket = 'PGE_CSV_DATA'
org = 'praveenkumar23.anguru@gmail.com'
pge_n_steps = 7

hours_per_month = 730
hours_per_day = 24
days_per_month = 30
num_bulbs = 2

# create client to run influx queries
def create_influx_client(bucket):
    token = 'uaElnni__FwThkojQgBlw069cZzqFiehCwog5QmiSsOKPSSdEj7O1PK8qDd_alm253SL8ZHj6PRhKuUclUXDDw=='
    account_number = '863594456'
    return InfluxDBClient(url='https://us-central1-1.gcp.cloud2.influxdata.com', token=token, verify_ssl=False)

# query the last N days and sum total PGE cost
def query_field(client, bucket, org, steps):
    query = f"""
        from(bucket: \"{bucket}\")
        |> range(start: -30d)
        |> timeShift(duration: -7h)
        |> filter(fn:(r) => r._measurement == \"pge_reading\")
        |> filter(fn:(r) => r._field == \"cost\")
        |> filter(fn:(r) => r.account_number == \"863594456\")
        |> drop(columns:["table", "_start", "_stop", "_field", "_measurement", "account_number", "result"])
    """
    tables = client.query_api().query(query, org=org)

    records = []
    for record in tables[0]:
      records.append({'time': record.values['_time'], 'cost': record.values['_value']})

    df = pd.DataFrame(records)
    df['time'] = df['time'].dt.round('D')
    df = df.groupby(['time']).agg({'cost': 'sum'}).reset_index()

    return df['cost'].tolist()[-steps:]

# load ARIMS model from pickle file
def load_LIFX_model(filename):
    return pickle.load(open(filename, 'rb'))

# load Keras LSTM model from JSON + H5 file
def load_PGE_model(model_filename, weights_filename):
    # load json and create model
    json_file = open(model_filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(weights_filename)
    loaded_model.compile(optimizer='adam', loss='mse')
    print('Loaded model from disk')

    return loaded_model

# create models for predictions in endpoints
LIFX_model = load_LIFX_model(LIFX_filename)
PGE_model = load_PGE_model(PGE_filename, PGE_weights)
client = create_influx_client(bucket)
max_steps = 10

@app.route('/predict/LIFX/')
def getLIFXForecast():
    interval = request.args.get('interval')

    if (request.args.get('steps') != None):
        steps = min(int(request.args.get('steps')), max_steps)
    else:
        steps = 1

    forecasts = LIFX_model.forecast(steps=steps).tolist()
    data = []
    for forecast in forecasts:
        if interval == 'days':
            data.append(forecast * num_bulbs * hours_per_day)
        elif interval == 'months':
            data.append(forecast * num_bulbs * hours_per_month)
        else:
            return {error: '{0} interval is not supported'.format(interval)}

    return json.dumps({
        'data': data,
        'interval_length': steps,
        'interval_unit': interval
    })

@app.route('/predict/PGE/')
def getPGEForecast():
    # get the next forecast based on the last 7 days
    previous_costs = query_field(client, bucket, org, pge_n_steps)

    # get interval unit from query
    interval = request.args.get('interval')

    if (request.args.get('steps') != None):
        steps = min(int(request.args.get('steps')), max_steps)
    else:
        steps = 1

    data = []
    for i in range(steps):
        input_data = np.array([previous_costs])
        input_data = input_data.reshape((input_data.shape[0], input_data.shape[1], 1))
        forecast = math.fabs(float(PGE_model.predict(input_data)[0][0]))

        # convert based on interval
        # forecasts are daily by default
        if (interval == 'days'):
            data.append(forecast)
        elif (interval == 'months'):
            data.append(forecast * days_per_month)
        else:
            return { 'error': '{0} interval is not supported'.format(interval) }

        # remove first item, add forecast, and get the next prediction
        previous_costs.pop(0)
        previous_costs.append(forecast)

    return json.dumps({
        'data': data,
        'interval_length': steps,
        'interval_unit': interval
    })

@app.route('/')
def welcome():
    return 'API for forecasting LIFX bulb and smart meter data. https://github.com/smannan/LIFXBulbAPI'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

















