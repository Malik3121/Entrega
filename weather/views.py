

# weather/views.py
from rest_framework import generics, permissions, viewsets
from .models import City, Weather
from .serializers import CitySerializer, WeatherSerializer
import openmeteo_requests

class CityViewSet(viewsets.ModelViewSet):
    # A viewset for the city model
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WeatherViewSet(viewsets.ModelViewSet):
    # A viewset for the weather model
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Get the weather data from openmeteo-requests and save it to the database
        city = self.request.data.get("city")
        city_obj = City.objects.get(id=city)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": city_obj.latitude,
            "longitude": city_obj.longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall"],
            "timezone": city_obj.timezone,
            "forecast_days": 1
        }
        response = openmeteo_requests.weather_api(url, params=params)[0]
        current = response.Current()
        weather_data = {
            "city": city,
            "temperature": current.Variables(0).Value(),
            "humidity": current.Variables(1).Value(),
            "precipitation": current.Variables(4).Value(),
            "rain": current.Variables(5).Value(),
            "showers": current.Variables(6).Value(),
            "snowfall": current.Variables(7).Value(),
        }
        serializer.save(**weather_data)
