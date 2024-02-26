import requests
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
import json
import time


def gen_metric():
    res = requests.get('http://api.open-notify.org/iss-now')
    response1 = res.json()
    #print(response1)
    json_object = json.dumps(response1, indent=4)

    payload = {"latitude": (response1['iss_position']['latitude']),
               "longitude": (response1['iss_position']['longitude']), "timestamp": (response1['timestamp'])}
    r = requests.post("http://127.0.0.1:5000/parse_request", json=payload)
    return payload


app = Flask(__name__)

# group by endpoint rather than path
metrics = PrometheusMetrics(app, group_by='endpoint')

@app.route('/parse_request', methods=['GET', 'POST'])
@metrics.gauge(
    'iss_location', 'Get location iss', labels={
        'latitude': lambda: request.json['latitude'],
        'longitude': lambda: request.json['longitude'],
        'timestamp': lambda: request.json['timestamp']
    })
def parse_request():
    return "ok"


@app.route('/')
def test():
    data = gen_metric()
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = data['timestamp']
    print("!!!")
    return '''<p>International Space Station Location</p>   
                    <p> latitude   value is: {}</p>  
                    <p> longitude  value is: {}</p>                    <p> timestamp  value is: {}'''.format(latitude, longitude, timestamp)
    # return gen_metric()


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
