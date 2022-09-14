from django.contrib import admin

from .models import Author, Book, Genre, ImageBook, PersonReader

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(ImageBook)
admin.site.register(Author)
admin.site.register(PersonReader)
