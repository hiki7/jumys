# vacancies/admin.py

from django.contrib import admin
from .models import Vacancy, Position, EmploymentType, Technology

admin.site.register(Vacancy)
admin.site.register(Position)
admin.site.register(EmploymentType)
admin.site.register(Technology)
