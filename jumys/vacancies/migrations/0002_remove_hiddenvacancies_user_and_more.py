# Generated by Django 5.1.1 on 2024-10-21 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hiddenvacancies',
            name='user',
        ),
        migrations.RemoveField(
            model_name='hiddenvacancies',
            name='vacancy',
        ),
        migrations.DeleteModel(
            name='HiddenCompanies',
        ),
        migrations.DeleteModel(
            name='HiddenVacancies',
        ),
    ]
