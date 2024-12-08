from rest_framework import serializers
from .models import Vacancy, Position, EmploymentType, Technology

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('name',)

class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ('name',)

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ('technology_name',)

class VacancySerializer(serializers.ModelSerializer):
    position_name = PositionSerializer()
    employment_type = EmploymentTypeSerializer(many=True)
    technology = TechnologySerializer(many=True)
    applications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    bookmarked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = '__all__'

    def create(self, validated_data):
        position_data = validated_data.pop('position_name')
        employment_types_data = validated_data.pop('employment_type')
        technologies_data = validated_data.pop('technology')

        position, created = Position.objects.get_or_create(name=position_data['name'])
        vacancy = Vacancy.objects.create(position_name=position, **validated_data)

        for employment_type_data in employment_types_data:
            employment_type, created = EmploymentType.objects.get_or_create(name=employment_type_data['name'])
            vacancy.employment_type.add(employment_type)

        for technology_data in technologies_data:
            technology, created = Technology.objects.get_or_create(technology_name=technology_data['technology_name'])
            vacancy.technology.add(technology)

        return vacancy

    def update(self, instance, validated_data):
        position_data = validated_data.pop('position_name', None)
        employment_types_data = validated_data.pop('employment_type', None)
        technologies_data = validated_data.pop('technology', None)

        if position_data:
            position, created = Position.objects.get_or_create(name=position_data['name'])
            instance.position_name = position

        if employment_types_data:
            instance.employment_type.clear()
            for employment_type_data in employment_types_data:
                employment_type, created = EmploymentType.objects.get_or_create(name=employment_type_data['name'])
                instance.employment_type.add(employment_type)

        if technologies_data:
            instance.technology.clear()
            for technology_data in technologies_data:
                technology, created = Technology.objects.get_or_create(
                    technology_name=technology_data['technology_name'])
                instance.technology.add(technology)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance