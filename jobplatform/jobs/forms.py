from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, RecruiterProfile, JobSeekerProfile, JobPosting, Application

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_description', 'phone_number']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['full_name', 'headline', 'resume_file', 'skills']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'resume_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'location', 'salary', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter_text']
        widgets = {
            'cover_letter_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
