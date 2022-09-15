from django.urls import path

from .views import (page_index, image_add, add_reader, add_author,
                    book_genre_popup_add, book_author_popup_add, readers_page,
                    BookListView, GetDiscriptionBook, search_result,
                    give_book, give_book_to_person, return_book, return_book_to_biblio, get_person, create_person,
                    update_person, delete_person)

app_name = 'lib'

urlpatterns = [
    path('register_book/', page_index, name='page_index'),
    path('image_add/', image_add, name='image_add'),
    # path('', main_page, name='main_page'),
    path('add_reader/', add_reader, name='add_reader'),
    path('add_author/', add_author, name='add_author'),
    path('register_book1/', book_genre_popup_add, name='book_genre_popup_add'),
    path('register_book2/', book_author_popup_add, name='book_author_popup_add'),
    path('readers/', readers_page, name='readers_page'),
    path('', BookListView.as_view(), name='main_page'),
    path('book/<int:pk>', GetDiscriptionBook.as_view(), name='get_discription_book'),
    path('search/', search_result, name='search'),
    path('give_book/', give_book, name='give_book'),
    path('give_book/<int:pk>', give_book_to_person, name='give_book_to_person'),
    path('return/', return_book, name='return_book'),
    path('return/<int:pk>', return_book_to_biblio, name='return_book_to_biblio'),
    path('get_person', get_person, name='get_person'),
    path('create_person', create_person, name='create_person'),
    path('update_person', update_person, name='update_person'),
    path('delete_person', delete_person, name='delete_person'),

]
