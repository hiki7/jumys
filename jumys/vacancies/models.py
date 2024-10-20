from django.contrib.auth.models import User
from django.db import models

CURRENCY = [("KZT", "₸"), ("RUB", "₽"), ("EUR", "€"), ("USD", "$")]

class Vacancy(models.Model):
    position_name = models.ForeignKey('Position', on_delete=models.CASCADE)
    salary_start = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_end = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY, default="KZT")
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    employment_type = models.ManyToManyField('EmploymentType', blank=True)
    technology = models.ManyToManyField('Technology', blank=True)
    is_active = models.BooleanField(default=True)

class Company(models.Model):
    name = models.CharField(max_length=255)
    company_description = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

class Location(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey('Street', on_delete=models.CASCADE, null=True, blank=True)

class Country(models.Model):
    name = models.CharField(max_length=255)

class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class Street(models.Model):
    name = models.CharField(max_length=255)

class EmploymentType(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Technology(models.Model):
    technology_name = models.CharField(max_length=255, unique=True)

class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

# Hidden Companies (Main app - vacancies)
class HiddenCompanies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Hidden Companies"
        verbose_name = "Hidden Company"

    def __str__(self):
        return f"{self.user.username} hides {self.company.name}"

# Hidden Vacancies (Main app - vacancies)
class HiddenVacancies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Hidden Vacancies"
        verbose_name = "Hidden Vacancy"

    def __str__(self):
        return f"{self.user.username} hides {self.vacancy.position_name}"
