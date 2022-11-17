from django.db import models


# Create your models here.
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=100)
    pseudonym_name = models.CharField(max_length=100)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='images', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
