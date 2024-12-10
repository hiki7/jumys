# companies/forms.py

from django import forms
from .models import Company, Location, Country, City, Street
from users.models import CustomUser

class AddManagerForm(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='hr'),
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
        fields = ['name', 'company_description', 'country_name', 'city_name', 'street_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'location') and self.instance.location:
            self.fields['country_name'].initial = self.instance.location.country.name
            self.fields['city_name'].initial = self.instance.location.city.name if self.instance.location.city else ''
            self.fields['street_name'].initial = self.instance.location.street.name if self.instance.location.street else ''

    def clean(self):
        cleaned_data = super().clean()
        country_name = cleaned_data.get('country_name')
        city_name = cleaned_data.get('city_name')

        if not country_name:
            self.add_error('country_name', 'Country name is required.')
        
        if not city_name:
            self.add_error('city_name', 'City name is required.')

        return cleaned_data
