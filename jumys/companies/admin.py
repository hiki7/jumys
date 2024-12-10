# companies/admin.py

from django.contrib import admin
from .models import Company, Location, Country, City, Street

admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Street)
