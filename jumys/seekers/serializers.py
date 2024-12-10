from rest_framework import serializers
from seekers.models import Ability

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['id', 'technology', 'experience_years', 'proficiency_level']
