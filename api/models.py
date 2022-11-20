from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

from bookstore.validator import alphanumeric_with_space_validator


class Author(models.Model):
    name = models.CharField(max_length=50, validators=[alphanumeric_with_space_validator])
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User',
                                 blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("name", "added_by"),)
        verbose_name = _('Author')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='images', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Book')


class RestrictUser(models.Model):
    restrict_author = models.ForeignKey(Author, help_text='All user in this list restrict to publish new book!',
                                        on_delete=models.CASCADE)
