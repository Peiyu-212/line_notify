from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50, null=False)
    iso2 = models.CharField(max_length=2, null=False)
    iso3 = models.CharField(max_length=3, null=False)


class City(models.Model):
    name = models.CharField(max_length=50, null=False)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    population = models.IntegerField()
    capital = models.CharField(max_length=10, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
