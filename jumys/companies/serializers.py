from rest_framework import serializers
from .models import Company, Location, Country, City, Street
from users.models import CustomUser

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'country')

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ('name',)

class LocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()
    street = StreetSerializer()

    class Meta:
        model = Location
        fields = ('country', 'city', 'street')

class CompanySerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    head_manager = serializers.ReadOnlyField(source='head_manager.username')

    class Meta:
        model = Company
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        country_data = location_data.pop('country')
        city_data = location_data.pop('city')
        street_data = location_data.pop('street')

        country, created = Country.objects.get_or_create(name=country_data['name'])
        city, created = City.objects.get_or_create(country=country, name=city_data['name'])
        street, created = Street.objects.get_or_create(name=street_data['name'])
        location, created = Location.objects.get_or_create(country=country, city=city, street=street)

        company = Company.objects.create(location=location, head_manager=self.context['request'].user, **validated_data)
        return company
