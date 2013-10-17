from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(
        widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label="Repeat your password")

    def clean_email(self):
        """Makes sure this email is unique"""
        if 'email' in self.cleaned_data:
            try:
                User.objects.get(email__iexact=self.cleaned_data['email'])
            except User.DoesNotExist:
                return self.cleaned_data['email']
            else:
                raise forms.ValidationError(
                    'This email has already been registered')

    def clean(self):
        """Make sure the passwords are equal."""
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password1') and cleaned_data.get('password2'):
            if not cleaned_data['password1'] == cleaned_data['password2']:
                raise forms.ValidationError('Passwords are not the same')
            return cleaned_data
        raise forms.ValidationError('Passwords are required.')
