from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm

from .customwidget import DateSelectorWidget
from .models import Author, Book, Genre, ImageBook, NewPerson, PersonReader, PersonCourse, PersonDisciplines


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


"""
crud ModelForm
"""
class NewPersonModelForm(ModelForm):
    class Meta:
        model = NewPerson
        fields = '__all__'
        widgets = {
            'disciplines': forms.CheckboxSelectMultiple()
        }


"""
crud Form
"""
class NewPersonForm(forms.Form):
    name = forms.CharField(max_length=127)
    last_name = forms.CharField(max_length=127)
    age = forms.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(0)])
    email = forms.EmailField(max_length=127)
    disciplines = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                 queryset=PersonDisciplines.objects.all())
    course = forms.ModelChoiceField(widget=forms.Select,  queryset=PersonCourse.objects.all())
    person_id = forms.CharField(widget=forms.HiddenInput())

    def save(self):
        person = NewPerson.objects.create(name=self.cleaned_data['name'],
                                     last_name=self.cleaned_data['last_name'],
                                     age=self.cleaned_data['age'],
                                     email=self.cleaned_data['email'],
                                     course_id=self.cleaned_data['course'].id)
        for i in self.cleaned_data['disciplines']:
            person.disciplines.add(i)
        return person

    def update(self):
        person = NewPerson.objects.get(id=self.cleaned_data['person_id'])
        person.name = self.cleaned_data['name']
        person.last_name = self.cleaned_data['last_name']
        person.age = self.cleaned_data['age']
        person.email = self.cleaned_data['email']
        person.course_id = self.cleaned_data['course'].id
        person.disciplines.set(self.cleaned_data['disciplines'])
        person.save()
        return person
