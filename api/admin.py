
# Register your models here.
from api.models import Author, Book, RestrictUser
from django.contrib import admin

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(RestrictUser)
