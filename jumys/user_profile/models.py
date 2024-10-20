from django.db import models
from django.conf import settings  # You can remove this if you use `CustomUser` directly
from django.utils import timezone
from users.models import CustomUser
from vacancies.models import Vacancy, Company, Position

# User Profile model to store additional user details
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone field
    links = models.TextField(blank=True, null=True)  # Links as a comma-separated string or JSONField
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Resume file upload
    abilities = models.ManyToManyField('Ability', blank=True, related_name='users')  # Many-to-Many with abilities
    bookmarked_vacancies = models.ManyToManyField(Vacancy, blank=True, related_name='bookmarked_by')
    applied_vacancies = models.ManyToManyField('Application', blank=True, related_name='applicants')

    def __str__(self):
        return self.user.email

# Ability model to track user skills
class Ability(models.Model):
    ABILITY_LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('expert', 'Expert'),
    ]

    technology = models.CharField(max_length=255)  # Technology name
    experience_years = models.IntegerField()  # Years of experience
    proficiency_level = models.CharField(max_length=20, choices=ABILITY_LEVEL_CHOICES, default='junior')

    class Meta:
        unique_together = ('technology', 'experience_years', 'proficiency_level')  # Avoid duplicate ability entries
        ordering = ['technology']  # Ordering by technology name for easier sorting

    def __str__(self):
        return f"{self.technology} - {self.proficiency_level} ({self.experience_years} years)"

# Work Experience model for user work history
class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experience')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Can be ongoing (end_date is optional)
    description = models.TextField(blank=True, null=True)
    reference = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='references')  # Optional reference to another user
    abilities = models.ManyToManyField(Ability, blank=True, related_name='work_experience')

    def __str__(self):
        ongoing = "Ongoing" if not self.end_date else f"Ended {self.end_date}"
        return f"{self.user_profile.user.email} - {self.company.name} ({self.position.name}) [{ongoing}]"

    class Meta:
        ordering = ['-start_date']  # Ordering by most recent experience first

# Application model to track applied vacancies
class Application(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_profile.user.email} applied for {self.vacancy.position_name} at {self.vacancy.company.name}"

    class Meta:
        ordering = ['-applied_on']  # Show the most recent applications first
