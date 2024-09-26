# File: apps/users/forms.py

from django import forms
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile

class EditProfileForm(forms.ModelForm):
    # Field dari model User
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    # Field dari model UserProfile
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    country = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    postal_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    company = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}))
    about = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About me', 'rows': 4}))
    foto_profile = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProfile
        fields = ['city', 'address', 'country', 'postal_code', 'about', 'company', 'foto_profile']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Ambil data user
        super(EditProfileForm, self).__init__(*args, **kwargs)

        if user:
            # Inisialisasi field dari model User
            self.fields['username'] = forms.CharField(
                initial=user.username,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
            )
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            super(EditProfileForm, self).save(commit=True)
        return user
