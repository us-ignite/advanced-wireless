from StringIO import StringIO

from django import forms
from django.core import validators
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from us_ignite.common import output, csv_unicode as csv
from us_ignite.profiles.models import Profile, ProfileLink, Interest


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
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
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'website', 'quote', 'bio',
                  'skills', 'availability', 'interests', 'interests_other',
                  'tags', 'is_public', 'position')

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    def save(self, *args, **kwargs):
        profile = super(ProfileForm, self).save(*args, **kwargs)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return profile


ProfileLinkFormSet = inlineformset_factory(
    Profile, ProfileLink, max_num=3, extra=3, can_delete=False)


class InviterForm(forms.Form):
    """Form to invite users to use the US Ignite site."""
    users = forms.CharField(widget=forms.Textarea,
                            help_text='Users must be in a ``name, email`` '
                            'format each new user must be in a new line.')

    def _validate_user(self, row):
        try:
            # Unpack the row
            name, email = row
        except (ValueError, TypeError):
            raise forms.ValidationError(
                '``%s`` has an invalid format. Must be ``name, email``'
                % ','.join(row))
        # Remove email whitespace:
        email = email.replace(' ', '')
        try:
            validators.validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Invalid email: ``%s``' % email)
        return (name, email)

    def clean_users(self):
        """Prepares the users to be imported.

        The output will be a list of tuples of name and email address::

            [('Name', 'Email address')]
        """
        if self.cleaned_data.get('users'):
            users_csv = csv.UnicodeReader(
                StringIO(self.cleaned_data.get('users')))
            cleaned_users = []
            for row in users_csv:
                if not row:
                    continue
                user_row = self._validate_user(row)
                if user_row:
                    cleaned_users.append(user_row)
            return cleaned_users


class UserExportForm(forms.Form):
    """Form used to filter the exported users."""
    start = forms.DateTimeField(
        required=False, widget=widgets.AdminSplitDateTime())
    end = forms.DateTimeField(
        required=False, widget=widgets.AdminSplitDateTime())

    def clean(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if (start and end) and (start > end):
            raise forms.ValidationError(
                'Start date is later than the end date.')
        return self.cleaned_data
