from django import forms

class SearchForm(forms.Form):
    query = forms.CharField()

class NewEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

class EditContentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)