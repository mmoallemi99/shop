from django import forms
from .models import Book


class EmailPostForm(forms.Form):
    class Meta:
        model = Book
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
