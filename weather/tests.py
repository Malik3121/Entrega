
# weather/tests.py
import requests
import unittest

class TestWeatherAPI(unittest.TestCase):
    # A test class for the weather API
    base_url = "http://127.0.0.1:8000/api/" # The base URL of the API

    def test_get_cities(self):
        # Test the GET /api/cities/ endpoint
        response = requests.get(self.base_url + "cities/")
        self.assertEqual(response.status_code, 200) # Check the status code
        self.assertEqual(len(response.json()), 2) # Check the number of cities
        self.assertEqual(response.json()[0]["name"], "Bishkek") # Check the name of the first city
        self.assertEqual(response.json()[0]["country"], "Kyrgyzstan") # Check the country of the first city

    def test_get_weather(self):
        # Test the GET /api/weather/ endpoint
        response = requests.get(self.base_url + "weather/")
        self.assertEqual(response.status_code, 200) # Check the status code
        self.assertEqual(len(response.json()), 2) # Check the number of weather data
        self.assertEqual(response.json()[0]["city"]["name"], "Bishkek") # Check the name of the city for the first weather data
        self.assertEqual(response.json()[0]["city"]["country"], "Kyrgyzstan") # Check the country of the city for the first weather data
        self.assertTrue(response.json()[0]["temperature"] > 0) # Check the temperature is positive

    def test_post_city(self):
        # Test the POST /api/cities/ endpoint
        data = {
            "name": "Tokyo",
            "country": "Japan",
            "latitude": 35.68,
            "longitude": 139.76,
            "timezone": "Asia/Tokyo"
        }
        response = requests.post(self.base_url + "cities/", data=data)
        self.assertEqual(response.status_code, 201) # Check the status code
        self.assertEqual(response.json()["name"], "Tokyo") # Check the name of the created city
        self.assertEqual(response.json()["country"], "Japan") # Check the country of the created city

    def test_post_weather(self):
        # Test the POST /api/weather/ endpoint
        data = {
            "city": 3 # The id of the city to get the weather data for
        }
        response = requests.post(self.base_url + "weather/", data=data)
        self.assertEqual(response.status_code, 201) # Check the status code
        self.assertEqual(response.json()["city"]["name"], "Tokyo") # Check the name of the city for the created weather data
        self.assertEqual(response.json()["city"]["country"], "Japan") # Check the country of the city for the created weather data
        self.assertTrue(response.json()["temperature"] > 0) # Check the temperature is positive

if __name__ == "__main__":
    unittest.main()
