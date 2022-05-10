from django.contrib import admin

from book.models import Book
from .models import Book
# Register your models here.
admin.site.register(Book)