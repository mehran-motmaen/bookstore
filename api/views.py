from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from rest_framework import viewsets, status, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'author__name']
    ordering = ['name']
    http_method_names = ['post', 'get', 'put', 'delete']

    def get_permissions(self):
        """Returns the permission based on the type of action"""

        if self.action == "list":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def get_renderers(self):

        if self.request.content_type == 'application/xml':
            self.renderer_classes = (XMLRenderer,)
        else:
            self.renderer_classes = (JSONRenderer,)
        return super().get_renderers()

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


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    ordering = ['name']
    http_method_names = ['post', 'get', 'put', 'delete']

    def get_renderers(self):
        if self.request.content_type == 'application/xml':
            self.renderer_classes = (XMLRenderer,)
        else:
            self.renderer_classes = (JSONRenderer,)

        return super().get_renderers()
