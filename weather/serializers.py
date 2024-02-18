
# weather/serializers.py
from rest_framework import serializers
from .models import City, Weather

class CitySerializer(serializers.ModelSerializer):
    # A serializer for the city model
    class Meta:
        model = City
        fields = ("id", "name", "country")

class WeatherSerializer(serializers.ModelSerializer):
    # A serializer for the weather model
    city = CitySerializer(read_only=True) # Show the city details

    class Meta:
        model = Weather
        fields = ("id", "city", "temperature", "humidity", "precipitation", "rain", "showers", "snowfall", "created")