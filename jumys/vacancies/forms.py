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


from companies.models import Company

class VacancyForm(forms.ModelForm):
    position_name = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Position"
    )
    employment_type = forms.ModelMultipleChoiceField(
        queryset=EmploymentType.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    technology = forms.ModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Company"
    )
    
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
            "location": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VacancyForm, self).__init__(*args, **kwargs)
        if self.user:
            if self.user.role == 'admin':
                self.fields['company'].queryset = Company.objects.all()
            elif self.user.role == 'hr':
                self.fields['company'].queryset = self.user.companies_managed.all()
            else:
                self.fields['company'].queryset = Company.objects.none()

    def clean_company(self):
        company = self.cleaned_data.get('company')
        if self.user and self.user.role == 'hr' and not self.user.companies_managed.filter(id=company.id).exists():
            raise forms.ValidationError("You do not have permission to create a vacancy for this company.")
        return company

