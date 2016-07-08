from django import forms

class EmailForm(forms.Form):
    firstname = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'required': ''}))
    lastname = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'required': ''}))
    organization = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Organization', 'required': ''}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'required': ''}))
    email_list = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'hidden', 'value': 'awt', 'id': ''}))

class PawrEmailForm(forms.Form):
    pawr_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'required': ''}))
    email_list = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'hidden', 'value': 'default', 'id': ''}))