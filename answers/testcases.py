import unittest
from answers.P4api import app

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_weather_data_page_1(self):
        response = self.client.get('/api/weather?station_id=USC00110072&start_date=1985-01-05&end_date=1985-01-06&page=1')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here for structure of response

    def test_get_weather_data_page_2(self):
        response = self.client.get('/api/weather?station_id=USC00110072&start_date=1985-01-05&end_date=1985-01-06&page=2')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here for structure of response

    def test_get_weather_data_no_end_date(self):
        response = self.client.get('/api/weather?station_id=USC00110072&start_date=1985-01-05')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here for structure of response

    def test_get_weather_data_long_range(self):
        response = self.client.get('/api/weather?station_id=USC00110072&start_date=1985-01-05&end_date=1985-12-01&page=1')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here for structure of response

    def test_get_weather_stats(self):
        response = self.client.get('/api/weather/stats?station_id=USC00110072&year=1985')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here for structure of response

if __name__ == '__main__':
    unittest.main()
