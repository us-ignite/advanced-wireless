from django import forms


class ContactForm(forms.Form):
    title = forms.CharField(max_length=500)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)


class ContactEmailForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField(max_length=500)
    body = forms.CharField(max_length=5000, widget=forms.Textarea)
