# tests/test_services.py

# -*- coding: utf-8 -*-
import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from geopy.distance import geodesic


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers import app, db  # Flask uygulamasını ve SQLAlchemy nesnesini import edin
from services import LocationService, Location

class TestServices(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()
    #Mock objeler, gerçek objelerin yerine geçerek belli koşullar altında testlerin nasıl işleyeceğini kontrol etme imkanı sağlar. 
    @patch('services.LocationService.get_all_filtered_locations')
    def test_find_nearest_locations(self, mock_get_all_filtered_locations):
        # Sahte verilerle mock veri tabanı sorgusunu ayarladık.
        mock_locations = [
            Location(latitude='41.0082', longitude='28.9784', terminal_id='T1', town_id='ISTANBUL'),  # İstanbul
            Location(latitude='40.7128', longitude='-74.0060', terminal_id='T2', town_id='NEW YORK'),  # New York
            Location(latitude='48.8566', longitude='2.3522', terminal_id='T3', town_id='PARIS')    # Paris
        ]
        mock_get_all_filtered_locations.return_value = mock_locations

        service = LocationService()
        latitude, longitude = 41.0082, 28.9784  # İstanbul koordinatları
        nearest_locations = service.find_nearest_locations(latitude, longitude, count=2)

        self.assertEqual(len(nearest_locations), 2)
        self.assertEqual(nearest_locations[0].latitude, '41.0082')
        self.assertEqual(nearest_locations[0].longitude, '28.9784')

if __name__ == '__main__':
    unittest.main()
