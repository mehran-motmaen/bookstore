from django.contrib import admin

# Register your models here.
from api.models import Author, Book, RestrictUser

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(RestrictUser)