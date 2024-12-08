# Generated by Django 5.1.4 on 2024-12-06 12:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technology', models.CharField(max_length=255)),
                ('experience_years', models.IntegerField()),
                ('proficiency_level', models.CharField(choices=[('junior', 'Junior'), ('middle', 'Middle'), ('senior', 'Senior'), ('expert', 'Expert')], default='junior', max_length=20)),
            ],
            options={
                'ordering': ['technology'],
                'unique_together': {('technology', 'experience_years', 'proficiency_level')},
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancies.vacancy')),
            ],
            options={
                'ordering': ['-applied_on'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('links', models.TextField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('abilities', models.ManyToManyField(blank=True, related_name='users', to='seekers.ability')),
                ('applied_vacancies', models.ManyToManyField(blank=True, related_name='applicants', to='seekers.application')),
                ('bookmarked_vacancies', models.ManyToManyField(blank=True, related_name='bookmarked_by', to='vacancies.vacancy')),
            ],
        ),
    ]