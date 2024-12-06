from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser
from vacancies.models import Vacancy, Position
from companies.models import Company

class Ability(models.Model):
    ABILITY_LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('expert', 'Expert'),
    ]
    technology = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    proficiency_level = models.CharField(max_length=20, choices=ABILITY_LEVEL_CHOICES, default='junior')

    class Meta:
        unique_together = ('technology', 'experience_years', 'proficiency_level')
        ordering = ['technology']

    def __str__(self):
        return f"{self.technology} - {self.proficiency_level} ({self.experience_years} years)"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    links = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    abilities = models.ManyToManyField(Ability, blank=True, related_name='users')
    bookmarked_vacancies = models.ManyToManyField(Vacancy, blank=True, related_name='bookmarked_by')
    applied_vacancies = models.ManyToManyField('Application', blank=True, related_name='applicants')

    def __str__(self):
        return self.user.email

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experience')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    reference = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='references')
    abilities = models.ManyToManyField(Ability, blank=True, related_name='work_experience')

    def __str__(self):
        ongoing = "Ongoing" if not self.end_date else f"Ended {self.end_date}"
        return f"{self.user_profile.user.email} - {self.company.name} ({self.position.name}) [{ongoing}]"

    class Meta:
        ordering = ['-start_date']

class Application(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_profile.user.email} applied for {self.vacancy.position_name} at {self.vacancy.company.name}"

    class Meta:
        ordering = ['-applied_on']
