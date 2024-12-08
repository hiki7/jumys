from django import forms
from .models import Vacancy, Position, EmploymentType, Technology


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmploymentTypeForm(forms.ModelForm):
    class Meta:
        model = EmploymentType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['technology_name']
        widgets = {
            'technology_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VacancyForm(forms.ModelForm):
    position_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    employment_type = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    technology = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Vacancy
        fields = [
            "position_name",
            "salary_start",
            "salary_end",
            "currency",
            "company",
            "location",
            "employment_type",
            "technology",
            "is_active",
        ]
        widgets = {
            "salary_start": forms.NumberInput(attrs={"class": "form-control"}),
            "salary_end": forms.NumberInput(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        position_name = self.cleaned_data.pop('position_name')
        employment_type_data = self.cleaned_data.pop('employment_type', None)
        technology_data = self.cleaned_data.pop('technology', None)

        position, created = Position.objects.get_or_create(name=position_name)
        self.instance.position_name = position

        vacancy = super().save(commit=commit)

        if employment_type_data:
            employment_type_list = [name.strip() for name in employment_type_data.split(',')]
            vacancy.employment_type.clear()
            for et_name in employment_type_list:
                employment_type, created = EmploymentType.objects.get_or_create(name=et_name)
                vacancy.employment_type.add(employment_type)

        if technology_data:
            technology_list = [name.strip() for name in technology_data.split(',')]
            vacancy.technology.clear()
            for tech_name in technology_list:
                technology, created = Technology.objects.get_or_create(technology_name=tech_name)
                vacancy.technology.add(technology)

        return vacancy
