from django.urls import path

from .views import (page_index, image_add, add_reader, add_author,
                    book_genre_popup_add, book_author_popup_add, readers_page,
                    BookListView, GetDiscriptionBook, search_result,
                    give_book, give_book_to_person, return_book, return_book_to_biblio,
                    get_person, create_person, update_person, delete_person,
                    main_page, get_detail_person, get_car, create_car, delete_car, detail_car, update_car,
                    get_person_form, get_detail_person_form, create_form, update_form, delete_form)

app_name = 'lib'

urlpatterns = [
    path('register_book/', page_index, name='page_index'),
    path('image_add/', image_add, name='image_add'),
    path('', main_page, name='main_page'),
    path('add_reader/', add_reader, name='add_reader'),
    path('add_author/', add_author, name='add_author'),
    path('register_book1/', book_genre_popup_add, name='book_genre_popup_add'),
    path('register_book2/', book_author_popup_add, name='book_author_popup_add'),
    path('readers/', readers_page, name='readers_page'),
    # path('', BookListView.as_view(), name='main_page'),
    path('book/<int:pk>', GetDiscriptionBook.as_view(), name='get_discription_book'),
    path('search/', search_result, name='search'),
    path('give_book/', give_book, name='give_book'),
    path('give_book/<int:pk>', give_book_to_person, name='give_book_to_person'),
    path('return/', return_book, name='return_book'),
    path('return/<int:pk>', return_book_to_biblio, name='return_book_to_biblio'),
    # forms.ModelForm
    path('get_person/', get_person, name='get_person'),
    path('get_person/<int:id>/', get_detail_person, name='get_detail_person'),
    path('get_person/create_person/', create_person, name='create_person'),
    path('get_person/update_person/<int:id>/', update_person, name='update_person'),
    path('get_person/delete_person/<int:id>/', delete_person, name='delete_person'),
    # Only input
    path('get_car/', get_car, name='get_car'),
    path('get_car/<int:id>/', detail_car, name='detail_view'),
    path('get_car/create/', create_car, name='create_car'),
    path('get_car/update/<int:id>/', update_car, name='update_car'),
    path('get_car/delete/<int:id>/', delete_car, name='delete_car'),
    # forms.Form
    path('get_person_form/', get_person_form, name='get_person_form'),
    path('get_person_form/<int:id>/', get_detail_person_form, name='get_detail_person_form'),
    path('get_person_form/create_form/', create_form, name='create_form'),
    path('get_person_form/update_form/<int:id>/', update_form, name='update_form'),
    path('get_person_form/delete_form/<int:id>/', delete_form, name='delete_form'),

]
