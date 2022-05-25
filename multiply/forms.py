from django import forms
from .models import GenericFile


class SearchForm(forms.Form):
    search = forms.CharField(label='Search for make and model', max_length=100, required=False)
    download_csv_active = forms.BooleanField(initial=False, required=False)
    download_csv_sold = forms.BooleanField(initial=False, required=False)

    def get_data(self):
        data = self.cleaned_data['search']
        return data
    
    class Meta:
        model = GenericFile
        fields = ('item')

