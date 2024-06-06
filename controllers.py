import os
import psutil
from flask import Flask, request, jsonify, render_template
from services import LocationService
from models import db
from flask_cors import CORS
from prometheus_client import Counter, Summary, Gauge, generate_latest, REGISTRY
import requests
from dotenv import load_dotenv

load_dotenv()  # Çevresel değişkenleri yükleyin

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
CORS(app)  


# Her bir endpoint için yapılan toplam istek sayısını sayan Prometheus sayaç metriği
REQUEST_COUNT = Counter('request_count', 'Number of requests by endpoint', ['endpoint'])

# Her bir endpoint için yapılan isteklerin gecikme sürelerini özetleyen Prometheus özet metriği
REQUEST_LATENCY = Summary('request_latency_seconds', 'Latency of requests in seconds', ['endpoint'])

# CPU ve bellek kullanımı metriklerini ekleyin
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage in percent')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage in percent')

location_service = LocationService()

@app.before_request
def before_request():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

@app.route('/')
def index():
    with REQUEST_LATENCY.labels(endpoint='/').time():
        REQUEST_COUNT.labels(endpoint='/').inc()
        return render_template('index.html')

@app.route('/route-form')
def route_form():
    with REQUEST_LATENCY.labels(endpoint='/route-form').time():
        REQUEST_COUNT.labels(endpoint='/route-form').inc()
        return render_template('route_form.html')

@app.route('/find-route', methods=['POST'])
def find_route():
    with REQUEST_LATENCY.labels(endpoint='/find-route').time():
        REQUEST_COUNT.labels(endpoint='/find-route').inc()
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        
        directions, distance, duration = get_directions(start_location, end_location)
        
        return render_template('route_result.html', directions=directions, start_location=start_location, end_location=end_location, distance=distance, duration=duration)

def get_directions(start, end):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # Google Maps API anahtarınızı çevresel değişkenden alın
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&key={api_key}'
    response = requests.get(url)
    directions = response.json()
    
    if directions['status'] == 'OK':
        distance = directions['routes'][0]['legs'][0]['distance']['text']
        duration = directions['routes'][0]['legs'][0]['duration']['text']
        return directions, distance, duration
    else:
        return None, None, None

@app.route('/locations', methods=['GET'])
def get_all_locations():
    with REQUEST_LATENCY.labels(endpoint='/locations').time():
        REQUEST_COUNT.labels(endpoint='/locations').inc()
        locations = location_service.get_all_locations()
        return jsonify([location.to_dict() for location in locations])

@app.route('/locations/<string:town_id>', methods=['GET'])
def get_locations_by_town_id(town_id):
    with REQUEST_LATENCY.labels(endpoint=f'/locations/{town_id}').time():
        REQUEST_COUNT.labels(endpoint=f'/locations/{town_id}').inc()
        locations = location_service.get_locations_by_town_id(town_id)
        return jsonify([location.to_dict() for location in locations])

@app.route('/nearest-locations', methods=['GET'])
def find_nearest_locations():
    with REQUEST_LATENCY.labels(endpoint='/nearest-locations').time():
        REQUEST_COUNT.labels(endpoint='/nearest-locations').inc()
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        locations = location_service.find_nearest_locations(latitude, longitude)
        return jsonify([location.to_dict() for location in locations])

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)

if __name__ == '__main__':
    app.run(debug=True)
