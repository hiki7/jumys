from django import forms
from companies.models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'company_description', 'location']
