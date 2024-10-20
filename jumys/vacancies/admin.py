from django.contrib import admin
from .models import Vacancy, Company, Location, Country, City, Street, EmploymentType, Technology, Position

# Register your models here.

admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Street)
admin.site.register(EmploymentType)
admin.site.register(Technology)
admin.site.register(Position)
