FROM python:3.9.2
ADD . /python-flask
WORKDIR /python-flask/

RUN pip install tensorflow
RUN pip install flask-restplus
RUN pip install flask_cors
RUN pip install 'statsmodels==0.12.2'
RUN pip install influxdb_client
