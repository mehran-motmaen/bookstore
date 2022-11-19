from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied
from api.models import Book, RestrictUser


@receiver(pre_save, sender=Book)
def restrict_author_to_publish(sender, instance, **kwargs):

    user = RestrictUser.objects.filter(restrict_author = instance.author)
    if user:
        raise PermissionDenied()
