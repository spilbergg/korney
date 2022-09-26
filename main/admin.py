from django.contrib import admin

from .models import (Author, Book, Genre, ImageBook, NewPerson,
                     PersonReader, Auto, AutoShop, CategorAuto)

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(ImageBook)
admin.site.register(Author)
admin.site.register(PersonReader)
admin.site.register(NewPerson)
admin.site.register(Auto)
admin.site.register(AutoShop)
admin.site.register(CategorAuto)
