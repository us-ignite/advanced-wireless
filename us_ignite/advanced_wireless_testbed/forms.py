from django import forms


ATTRS = {
    'style': 'width:10em;'
}
class EmailForm(forms.Form):
    firstname = forms.CharField(required=True, widget=forms.TextInput(attrs={'cols': 100, 'style': 'width: 63em;'}))
    lastname = forms.CharField(required=True, widget=forms.TextInput(attrs=ATTRS))
    organization = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'width: 63em;'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'style': 'width: 63em;'}))
