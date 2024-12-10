from rest_framework import serializers
from .models import Vacancy, Position, EmploymentType, Technology

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']

class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ['id', 'name']

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'technology_name']

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            'id', 'position_name', 'salary_start', 'salary_end', 'currency',
            'company', 'location', 'employment_type', 'technology', 'is_active',
            'applications', 'created_at'
        ]
