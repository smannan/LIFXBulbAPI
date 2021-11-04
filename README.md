# LIFXBulbAPI
Dockerized Flask APIs to deploy forecasting models for LIFX Bulb and PG&amp;E smart meter data

Deploy ARIMA and LSTM models developed in repository https://github.com/smannan/LIFXBulbAnalysis for forecasting future
energy costs for LIFX bulbs and PG&E smart meters.

# Dependencies

Python 3.9.2

```
pip3 install tensorflow
pip3 install flask-restplus
pip3 install 'statsmodels==0.12.2'
pip3 install influxdb_client
```

# To run

```python3 api/app.py ```

# Request

```curl 'localhost:105/predict/LIFX/?steps=7&interval=months'```

```curl 'localhost:105/predict/PGE/?steps=7&interval=days'```

# Response

- data = list of forecasts (future costs)
- interval length = number of steps requested
- interval unit = months or days


```
{
   "data": [3.109279411338356,
            3.109294227093614,
            3.1092942594720308,
            3.10929425954279,
            3.1092942595429447,
            3.1092942595429456,
            3.1092942595429456],
   "interval_length": 7,
   "interval_unit": "months"
}
```
