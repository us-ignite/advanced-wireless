from django import forms


class TagSearchForm(forms.Form):
    tag = forms.CharField(max_length=50)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=50, label='Search')
