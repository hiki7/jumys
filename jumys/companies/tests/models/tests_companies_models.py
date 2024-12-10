from companies.models import Country, City, Street, Location, Company
from users.models import CustomUser
from companies.serializers import CompanySerializer, LocationSerializer
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from unittest.mock import patch
from companies.utils import get_location_from_nominatim

class CountryModelTest(TestCase):
    def test_country_str_method(self):
        country = Country.objects.create(name='Kazakhstan')
        self.assertEqual(str(country), 'Kazakhstan')

class CityModelTest(TestCase):
    def test_city_str_method(self):
        country = Country.objects.create(name='Kazakhstan')
        city = City.objects.create(name='Almaty', country=country)
        self.assertEqual(str(city), 'Almaty')

class StreetModelTest(TestCase):
    def test_street_str_method(self):
        street = Street.objects.create(name='Main Street')
        self.assertEqual(str(street), 'Main Street')

class LocationModelTest(TestCase):
    def test_location_str_method(self):
        country = Country.objects.create(name='Kazakhstan')
        city = City.objects.create(name='Almaty', country=country)
        street = Street.objects.create(name='Main Street')
        location = Location.objects.create(country=country, city=city, street=street, latitude=43.2567, longitude=76.9286)
        self.assertEqual(str(location), 'Almaty, Kazakhstan, Main Street')

class CompanyModelTest(TestCase):
    def test_company_str_method(self):
        user = CustomUser.objects.create(username='testuser', password='testpass123')
        country = Country.objects.create(name='Kazakhstan')
        city = City.objects.create(name='Almaty', country=country)
        street = Street.objects.create(name='Main Street')
        location = Location.objects.create(country=country, city=city, street=street)
        company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
        self.assertEqual(str(company), 'Test Company')

