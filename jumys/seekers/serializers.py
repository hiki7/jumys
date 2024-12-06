from rest_framework import serializers
from .models import UserProfile, Ability, WorkExperience, Application
from users.serializers import UserSerializer
from vacancies.serializers import VacancySerializer

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, required=False)

    class Meta:
        model = WorkExperience
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer()

    class Meta:
        model = Application
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, required=False)
    work_experience = WorkExperienceSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
