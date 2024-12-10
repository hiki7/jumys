# companies/forms.py

from django import forms
from .models import Company, Location, Country, City, Street
from users.models import CustomUser

class AddManagerForm(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='hr'),  # Adjust queryset as needed
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_user'}),
        required=True,
        label="Select Manager(s)"
    )

    
class CompanyForm(forms.ModelForm):
    country_name = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city_name = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    street_name = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Company
        fields = ['name', 'company_description']  # Removed 'country_name', 'city_name', 'street_name'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.location:
            self.fields['country_name'].initial = self.instance.location.country.name
            self.fields['city_name'].initial = self.instance.location.city.name if self.instance.location.city else ''
            self.fields['street_name'].initial = self.instance.location.street.name if self.instance.location.street else ''
