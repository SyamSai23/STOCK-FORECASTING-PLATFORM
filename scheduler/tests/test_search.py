import json
from flask_testing import TestCase

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WealthWingman.scheduler.finapp.__main__ import app
class TestSearchEndpoint(TestCase):
    def create_app(self):
        # Setup your Flask application for testing
        app.config['TESTING'] = True
        return app

    def test_search_tsla(self):
        # Send a POST request to the /search endpoint
        response = self.client.post('/search', 
                                    data=json.dumps({'ticker': 'TSLA'}),
                                    content_type='application/json')
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Pretty-print the response data
        response_data = json.loads(response.data.decode('utf-8'))
        print("Response Data (Pretty JSON):")
        print(json.dumps(response_data, indent=4))

        # Optionally, check for specific content in the response
        # Ensure the response includes TSLA information
        self.assertIn('TSLA', response_data['ticker'])