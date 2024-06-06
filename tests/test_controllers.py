# tests/test_controllers.py

# -*- coding: utf-8 -*-
import unittest
import sys
import os
from unittest.mock import patch

# Proje kök dizinini sys.path'e ekleyin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test etmek için get_directions fonksiyonunu controllers modülünden içe aktarın
from controllers import get_directions

# TestControllers sınıfı unittest.TestCase sınıfından miras alır
class TestControllers(unittest.TestCase):

    @patch('controllers.requests.get')
    def test_get_directions(self, mock_get):
        # Mock response data - Taklit edilen yanıt verileri
        mock_response = {
            'status': 'OK',
            'routes': [{
                'legs': [{
                    'distance': {'text': '10 km'},
                    'duration': {'text': '15 mins'}
                }]
            }]
        }
        # mock_get'in döndüreceği değeri ayarlayın
        mock_get.return_value.json.return_value = mock_response
        
        # get_directions fonksiyonunu test ediyoruz
        directions, distance, duration = get_directions('start', 'end')
        
        # Beklenen mesafe ve süre değerlerini doğrulayın
        self.assertEqual(distance, '10 km')
        self.assertEqual(duration, '15 mins')
        self.assertIsNotNone(directions)

# Bu dosya doğrudan çalıştırıldığında testleri çalıştırır
if __name__ == '__main__':
    unittest.main()
