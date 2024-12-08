from django import forms
from .models import UserProfile, Ability, WorkExperience, Application


class AbilityForm(forms.ModelForm):
    class Meta:
        model = Ability
        fields = ['technology', 'experience_years', 'proficiency_level']
        widgets = {
            'technology': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'proficiency_level': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkExperienceForm(forms.ModelForm):
    abilities = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = WorkExperience
        fields = ['company', 'position', 'start_date', 'end_date', 'description', 'abilities']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ApplicationForm(forms.ModelForm):
    vacancy = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Application
        fields = ['vacancy']
        widgets = {
            'vacancy': forms.Select(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    abilities = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )
    work_experience = forms.ModelMultipleChoiceField(
        queryset=WorkExperience.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'links', 'resume', 'abilities', 'work_experience']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'links': forms.Textarea(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
