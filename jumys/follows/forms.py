from django import forms
from .models import Follow, Connection, ReferenceLetter


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['followee']
        widgets = {
            'followee': forms.HiddenInput(),
        }


class ConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ['receiver']
        widgets = {
            'receiver': forms.HiddenInput(),
        }


class ReferenceLetterForm(forms.ModelForm):
    class Meta:
        model = ReferenceLetter
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your reference here...'}),
        }
