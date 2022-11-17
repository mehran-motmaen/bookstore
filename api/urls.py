from api.views import BookViewSet, AuthorViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'author', AuthorViewSet, basename='author')
