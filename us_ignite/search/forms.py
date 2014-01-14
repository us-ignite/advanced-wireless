from django import forms


class TagSearchForm(forms.Form):
    tag = forms.CharField(max_length=50)
