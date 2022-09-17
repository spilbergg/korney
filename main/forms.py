from django import forms
from django.forms import ModelForm

from .customwidget import DateSelectorWidget
from .models import Author, Book, Genre, ImageBook, NewPerson, PersonReader


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    # returns the book in lowercase
    def clean_name_book_rus(self):
        return self.cleaned_data['name_book_rus'].lower()


class BookFormGenre(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class BookFormAuthors(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class ImageBookForm(forms.ModelForm):
    class Meta:
        model = ImageBook
        fields = '__all__'


class PersonReaderForm(forms.ModelForm):
    class Meta:
        model = PersonReader
        fields = '__all__'

        widgets = {
            'date_birthday': DateSelectorWidget,
            'person_get_book': DateSelectorWidget,
        }


class Author_form(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class NewPersonForm(ModelForm):
    class Meta:
        model = NewPerson
        fields = '__all__'
