from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    role = forms.ChoiceField(
        choices=[
            ('candidate', 'Candidate'),
            ('recruiter', 'Recruiter'),
        ]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role'
        ]