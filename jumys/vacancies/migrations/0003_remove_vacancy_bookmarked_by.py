# Generated by Django 5.1.4 on 2024-12-08 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0002_vacancy_applications_vacancy_bookmarked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='bookmarked_by',
        ),
    ]