
import os 
import pickle

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from keras.models import model_from_json

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
LIFX_filename = '{0}/models/smart_bulb_arima.pkl'.format(dir_path)
PGE_filename = '{0}/models/pge_lstm_model.json'.format(dir_path)
PGE_weights = '{0}/models/pge_lstm_model_weights.h5'.format(dir_path)

def load_LIFX_model(filename):
    return pickle.load(open(filename, 'rb'))

def load_PGE_model(model_filename, weights_filename):
    # load json and create model
    json_file = open(model_filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(weights_filename)
    print('Loaded model from disk')

    return loaded_model

LIFX_model = load_LIFX_model(LIFX_filename)
PGE_model = load_PGE_model(PGE_filename, PGE_weights)

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