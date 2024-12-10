from rest_framework import serializers
from .models import Ability, UserProfile, WorkExperience, Application

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['id', 'technology', 'experience_years', 'proficiency_level']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone', 'links', 'resume', 'abilities', 'bookmarked_vacancies']

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['id', 'user_profile', 'company', 'position', 'start_date', 'end_date', 'description', 'reference', 'abilities']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'user_profile', 'vacancy', 'applied_on', 'reviewed']
