import requests

def get_location_from_nominatim(country_name, city_name, street_name=None):
    query_parts = []
    if street_name:
        query_parts.append(street_name)
    if city_name:
        query_parts.append(city_name)
    if country_name:
        query_parts.append(country_name)
    query = ", ".join(query_parts)

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    headers = {
        'User-Agent': 'YourAppName/1.0 (your.email@example.com)'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return None

    data = response.json()
    if not data:
        return None

    result = data[0]
    lat = result.get('lat')
    lon = result.get('lon')
    address = result.get('address', {})

    validated_country = address.get('country')
    validated_city = address.get('city') or address.get('town') or address.get('village')
    validated_street = address.get('road') if street_name else None

    if not validated_country or not validated_city:
        return None

    return {
        'country': validated_country,
        'city': validated_city,
        'street': validated_street,
        'latitude': lat,
        'longitude': lon
    }
