from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'search',
        'name': 'query',
        'placeholder': 'Поиск по статьям...'
    }))


# <input type="search" class="form-control" name="search-input" value="" placeholder="Поиск по статьям..." required >


