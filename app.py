from controllers import app  # controllers.py dosyasından Flask uygulamasını içe aktarın
from flask_cors import CORS

CORS(app)  # CORS politikasını etkinleştirin

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, host='0.0.0.0', port=5010)  # Flask uygulamasını başlatın
