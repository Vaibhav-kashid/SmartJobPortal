from django import forms
from .models import job
from account.models import Candidate


class jobForm(forms.ModelForm):

    class Meta:
        model = job
        fields = [
            'title',
            'company_name',
            'location',
            'description',
            'required_skills',
            'salary'
        ]


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = [
            'phone',
            'skills',
            'education',
            'resume'
        ]

        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter phone number'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'placeholder': 'Example: Python, Django, SQL',
                    'rows': 3
                }
            ),

            'education': forms.TextInput(
                attrs={
                    'placeholder': 'Example: BCA'
                }
            ),
        }