from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from us_ignite.profiles.models import Profile, ProfileLink


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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'website', 'bio')


ProfileLinkFormSet = inlineformset_factory(
    Profile, ProfileLink, max_num=3, extra=1)


class InviterForm(forms.Form):
    users = forms.CharField(widget=forms.Textarea,
                            help_text='Users must be in a ``name, email`` '
                            'format each new user must be in a new line.')

    def clean_users(self):
        """Prepares the users to be imported.

        The output will be a list of tuples of name and email address::

            [('Name', 'Email address')]
        """
        if self.cleaned_data.get('users'):
            rows = self.cleaned_data['users'].splitlines()
            rows = filter(None, rows)
            if not rows:
                raise forms.ValidationError('No users have been provided.')
            cleaned_users = []
            for r in rows:
                try:
                    name, email = r.split(',')
                except Exception, e:
                    raise forms.ValidationError(
                        '``%s`` has an invalid format. Must be ``name, email``'% r)
                # Remove email whitespace:
                email = email.replace(' ', '')
                try:
                    validators.validate_email(email)
                except forms.ValidationError:
                    raise forms.ValidationError('Invalid email: %s' % email)
                cleaned_users.append((name, email))
            return cleaned_users
