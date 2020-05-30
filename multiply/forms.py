from django import forms
from .models import GenericFile


class SearchForm(forms.Form):
    search = forms.CharField(label='Search for make and model', max_length=100)
    download_csv = forms.BooleanField(initial=False, required=False)

    def get_data(self):
        data = self.cleaned_data['search']
        return data
    
    class Meta:
        model = GenericFile

