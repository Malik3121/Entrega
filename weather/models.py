from django.db import models

class City(models.Model):
    # A city model that stores the name and country of a city
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.country}"

class Weather(models.Model):
    # A weather model that stores the weather data for a city
    city = models.ForeignKey(City, related_name="weather", on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
    rain = models.FloatField()
    showers = models.FloatField()
    snowfall = models.FloatField()
    created = models.DateTimeField(auto_now_add=True) # The date and time of the weather data creation

    class Meta:
        ordering = ("-created",) # Order by the most recent weather data

    def __str__(self):
        return f"Weather for {self.city} at {self.created}"