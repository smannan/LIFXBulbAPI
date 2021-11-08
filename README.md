# LIFXBulbAPI
Dockerized Flask APIs to deploy forecasting models for LIFX Bulb and PG&amp;E smart meter data

Deploy ARIMA and LSTM models developed in repository https://github.com/smannan/LIFXBulbAnalysis for forecasting future
energy costs for LIFX bulbs and PG&E smart meters.

# Dependencies

Docker - https://docs.docker.com/get-started/

To verify installation:
1. Start Docker desktop
2. Rum ```docker run -d -p 80:80 docker/getting-started```

# To run

```docker compose up```

# Request

```curl 'localhost:5000/predict/LIFX/?steps=7&interval=months'```

```curl 'localhost:5000/predict/PGE/?steps=7&interval=days'```

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

# Deploy

Push to Docker Hub https://docs.docker.com/docker-hub/

```
docker build -t smannan95/lifxbulbapi .
docker run -d -p 5000:5000 smannan95/lifxbulbapi
docker push smannan95/lifxbulbapi
```

Deploy on GCP: https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python


URL: https://lifxbulbapi-dk63ggrjhq-de.a.run.app


Ex
- ```https://lifxbulbapi-dk63ggrjhq-de.a.run.app/predict/PGE/?steps=7&interval=months```

- ```https://lifxbulbapi-dk63ggrjhq-de.a.run.app/predict/LIFX/?steps=7&interval=months```

