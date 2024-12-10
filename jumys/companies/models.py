from django.db import models
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Street(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey('Street', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.country}, {self.street}"



class Company(models.Model):
    name = models.CharField(max_length=255)
    company_description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    head_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companies_headed', null=True, blank=True)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='companies_managed', blank=True)

    def __str__(self):
        return self.name
