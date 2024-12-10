from django import forms

class CompanyForm(forms.Form):
    name = forms.CharField(max_length=255, label="Company Name")
    company_description = forms.CharField(widget=forms.Textarea, label="Description")
    country_name = forms.CharField(max_length=255, label="Country")
    city_name = forms.CharField(max_length=255, label="City")
    street_name = forms.CharField(max_length=255, required=False, label="Street (optional)")
