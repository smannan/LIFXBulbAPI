
import os 
import pickle

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
LIFX_model = pickle.load(open('{0}/models/smart_bulb_arima.pkl'.format(dir_path), 'rb'))

@app.route('/predict/LIFX/')
def getLIFXForecast():
    return {
        'cost': LIFX_model.forecast()[0],
        'interval_length': '1',
        'interval_unit': 'hour'
    }

@app.route('/predict/PGE/')
def getPGEForecast():
    return {
        'cost': 5,
        'interval_length': '1',
        'interval_unit': 'day'
    }

@app.route('/')
def welcome():
    return 'API for forecasting LIFX bulb and smart meter data. https://github.com/smannan/LIFXBulbAPI'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)