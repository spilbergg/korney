import datetime

from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import Author_form, BookFormGenre, BookFormAuthors, BookForm, ImageBookForm, PersonReaderForm, \
    NewPersonForm
from .models import Book, ImageBook, NewPerson, PersonReader, Auto
from .utils import discont


class BookListView(ListView):
    model = Book
    template_name = 'main_page.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Book.objects.get'
        return context


class GetDiscriptionBook(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ОписаниеКниги'
        return context


def page_index(request):
    form = BookForm()
    form_genre = BookFormGenre()
    form_authors = BookFormAuthors()
    context = {
        'form': form,
        'form_genre': form_genre,
        'form_authors': form_authors
    }
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            ImageBook.objects.create(
                photo_book=request.FILES['image'],
                books=book
            )
        else:
            erorr = form.errors
            context = {
                'form': form,
                'error': erorr,
            }
    return render(request, 'page_index.html', context)


def book_genre_popup_add(request):
    if request.method == 'POST':
        form1 = BookFormGenre(request.POST)
        if form1.is_valid():
            form1.save()

    return redirect('lib:page_index')


def book_author_popup_add(request):
    if request.method == 'POST':
        form1 = BookFormAuthors(request.POST, request.FILES)
        if form1.is_valid():
            form1.save()
    return redirect('lib:page_index')


def image_add(request):
    form = ImageBookForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = ImageBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            erorr = form.errors
            context = {
                'form': form,
                'error': erorr,
            }
    return render(request, 'image_add.html', context)


'''Не удалять и не коментить, сделал на ListView(эксперимент)'''


def main_page(request):
    books = Book.objects.all()
    paginator = Paginator(books, 1)
    page_number = request.GET.get('page', 1)
    title = 'Гавная страница'
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'main_page.html', {'page_obj': page_obj, 'title': title})


def add_reader(request):
    form = PersonReaderForm()

    context = {
        'form': form,
        'title': 'Добавление читателя',
    }
    if request.method == 'POST':
        form = PersonReaderForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            erorr = form.errors
            context = {
                'form': form,
                'error': erorr,
                'title': 'Добавление читателя',
            }
    return render(request, 'person_form.html', context)


def add_author(request):
    form = Author_form()
    context = {
        'form': form,
        'title': 'Добавление автора',
    }
    if request.method == 'POST':
        form = Author_form(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
        else:
            erorr = form.errors
            context = {
                'form': form,
                'error': erorr,
                'title': 'Добавление автора',
            }
    return render(request, 'author_form.html', context)


def readers_page(request):
    readers = PersonReader.objects.all()
    paginator = Paginator(readers, 1)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    context = {
        'readers': readers,
        'title': 'Читатели',
        'page_obj': page_obj,
    }
    return render(request, 'reades_page.html', context)


def search_result(request):
    if request.method == 'GET':
        search = request.GET['search'].casefold()
        result = Book.objects.filter(name_book_rus=search)
        context = {
            'book': result,
            'title': 'поиск',
        }

        return render(request, 'search.html', context)


def give_book(request):
    readers = PersonReader.objects.all()
    context = {
        'readers': readers
    }
    if request.method == 'POST':
        name = request.POST.get('search_reader')
        try:
            context = {
                'readers': [PersonReader.objects.get(first_name=name)]
            }
        except PersonReader.DoesNotExist:
            return redirect('lib:add_reader')
    return render(request, 'give_book.html', context)


def give_book_to_person(request, pk):
    books = Book.objects.all()
    context = {
        'books': books
    }
    reader = PersonReader.objects.get(pk=pk)
    # print(datetime.datetime.date(datetime.datetime.now()))
    if request.method == 'POST':
        if reader.book_set.all().exists():
            context = {
                'books': books,
                'error': 'данный читатель не сдал прошлые книги'
            }
        else:
            book = request.POST.getlist('books')
            if len(book) < 5 and len(book) > 0:

                for f in book:
                    one_book = Book.objects.get(name_book_rus=f)
                    if one_book.count_book > len(one_book.book_read_person.all()):
                        reader.book_set.add(one_book)
                    else:
                        book.remove(f)
                reader.person_get_book = datetime.datetime.date(datetime.datetime.now())
                reader.save()
                price = discont(book)
                context = {
                    'price': price
                }
                return render(request, 'book_to_reader.html', context)
            else:
                context = {
                    'books': books,
                    'error': 'введите корректное число книг'
                }
    return render(request, 'book_to_reader.html', context)


def return_book(request):
    names = set(PersonReader.objects.filter(book__book_read_person__isnull=False))
    context = {
        'names': names,
        'title': 'Список читателей',
    }
    return render(request, 'return_book.html', context)


def return_book_to_biblio(request, pk):
    reader = PersonReader.objects.get(pk=pk)
    books = reader.book_set.all()
    context = {
        'reader': reader,
        'books': books,
        'title': 'СписокКниг',
    }
    if request.method == 'POST':
        if len(request.POST) > 1:
            book_list = list(map(str.lower, request.POST.getlist('return_book_to_biblio')))
            # new_book_list = [x.lower() for x in request.POST.getlist('return_book_to_biblio')]
            for i in book_list:
                book = Book.objects.get(name_book_rus=i)
                reader.book_set.remove(book)
                print(book)
    return render(request, 'return_book_to_biblio.html', context)


# Simple implementation CRUD
def get_person(request):
    """cRud"""
    persons = NewPerson.objects.all()
    if not persons:
        # return redirect('lib:create_person')
        return render(request, 'crud/create.html')
    return render(request, 'crud/read.html', {'persons': persons})


def get_detail_person(request, id):
    try:
        data = NewPerson.objects.get(id=id)
    except NewPerson.DoesNotExist:
        raise Http404('Person not found')
    return render(request, 'crud/detail_person.html', {'data': data})


def create_person(request):
    """Crud"""
    if request.method == "POST":
        form = NewPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lib:get_person')
    else:
        form = NewPersonForm()
        context = {
            'form': form
        }
        return render(request, 'crud/create.html', context)


def update_person(request, id):
    """crUd"""
    try:
        person = get_object_or_404(NewPerson, id=id)
    except Exception:
        raise Http404('Person not found')
    if request.method == "POST":
        form = NewPersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('lib:get_person')
    else:
        form = NewPersonForm(instance=person)
        context = {
            'form': form
        }
        return render(request, 'crud/update.html', context)


def delete_person(request, id):
    """cruD"""
    try:
        person = get_object_or_404(NewPerson, id=id)
    except Exception:
        raise Http404('Person not found')
    if request.method == 'POST':
        person.delete()
        return redirect('lib:get_person')
    else:
        return render(request, 'crud/delete.html')


# CRUD  from Auto
def get_car(request):
    cars = Auto.objects.all()
    return render(request, 'crud_form/view.html', {'cars': cars})


def create_car(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        description = request.POST.get('description')
        color = request.POST.get('color')
        price = request.POST.get('price')
        if model and description and color:
            Auto.objects.create(
                model=model,
                description=description,
                color=color,
                price=price
            )
            return redirect('lib:get_car')
        else:
            return HttpResponse('<h1>Данные не корректны,'
                                ' пробуйте вводить сново если с первого '
                                'раза не можете </h1>')
    return render(request, 'crud_form/create.html')
