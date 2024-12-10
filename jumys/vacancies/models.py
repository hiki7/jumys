from django.db import models
from django.conf import settings
from companies.models import Company, Location

CURRENCY = [("KZT", "₸"), ("RUB", "₽"), ("EUR", "€"), ("USD", "$")]

class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class EmploymentType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Technology(models.Model):
    technology_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.technology_name

class Vacancy(models.Model):
    position_name = models.ForeignKey(Position, on_delete=models.CASCADE, db_index=True)
    salary_start = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_end = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY, default="KZT")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    employment_type = models.ManyToManyField(EmploymentType, blank=True)
    technology = models.ManyToManyField(Technology, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    applications = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="applied_vacancies",
        blank=True
    )

    def __str__(self):
        return f"{self.position_name.name} at {self.company.name}"
