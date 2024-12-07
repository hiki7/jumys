from rest_framework import serializers
from .models import Company, Location, Country, City, Street
from users.models import CustomUser
from ..core.utils import get_location_from_nominatim

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
    # Instead of passing nested serializers for location, we accept raw strings.
    country_name = serializers.CharField(write_only=True)
    city_name = serializers.CharField(write_only=True)
    street_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    
    # Read-only representation of location
    location = serializers.SerializerMethodField()
    head_manager = serializers.ReadOnlyField(source='head_manager.username')

    class Meta:
        model = Company
        fields = (
            'id', 'name', 'company_description', 'head_manager', 'managers',
            'location', 'country_name', 'city_name', 'street_name'
        )

    def get_location(self, obj):
        if obj.location:
            return {
                'country': obj.location.country.name,
                'city': obj.location.city.name if obj.location.city else None,
                'street': obj.location.street.name if obj.location.street else None,
                'latitude': str(obj.location.latitude),
                'longitude': str(obj.location.longitude)
            }
        return None

    def create(self, validated_data):
        request_user = self.context['request'].user
        country_name = validated_data.pop('country_name')
        city_name = validated_data.pop('city_name')
        street_name = validated_data.pop('street_name', None)

        # Call external API to validate and enrich location data
        location_data = get_location_from_nominatim(country_name, city_name, street_name)
        if not location_data:
            raise serializers.ValidationError("Invalid location data. Could not find coordinates for the provided country/city.")

        # Extract validated info
        validated_country = location_data['country']
        validated_city = location_data['city']
        validated_street = location_data['street']
        latitude = location_data['latitude']
        longitude = location_data['longitude']

        # Get or create the country
        country, _ = Country.objects.get_or_create(name=validated_country)
        # Get or create the city
        city, _ = City.objects.get_or_create(name=validated_city, country=country)
        
        # Street may be optional
        street = None
        if validated_street:
            street, _ = Street.objects.get_or_create(name=validated_street)
        
        # Get or create location
        location, created = Location.objects.get_or_create(
            country=country,
            city=city,
            street=street,
            defaults={'latitude': latitude, 'longitude': longitude}
        )
        # If not created, update coordinates if needed
        if not created:
            # You can decide if you want to update coordinates.
            location.latitude = latitude
            location.longitude = longitude
            location.save()

        company = Company.objects.create(location=location, head_manager=request_user, **validated_data)
        return company