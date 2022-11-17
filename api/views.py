from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, decorators, permissions
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer


@renderer_classes((JSONRenderer, XMLRenderer))
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ('name', 'description', 'author',)
    ordering = ('name',)
    http_method_names = ['post', 'get', 'put', 'delete']

    def get_permissions(self):
        """Returns the permission based on the type of action"""

        if self.action == "list":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        response = super(BookViewSet, self).list(request, *kwargs, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user.id
            book = self.get_object()

            if book.author.added_by.id == user:
                response = super().destroy(request, *args, **kwargs)

                return Response({'results': response.data}, status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'message': 'Action not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except ObjectDoesNotExist as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Something went wrong'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@renderer_classes((JSONRenderer, XMLRenderer))
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer
    search_fields = ('name',)
    ordering = ('name',)
    http_method_names = ['post', 'get', 'put', 'delete']
