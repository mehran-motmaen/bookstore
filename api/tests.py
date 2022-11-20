from django.test import TestCase

# Create your tests here.
from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from django.test import SimpleTestCase, Client
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Author, Book
from api.serializers import AuthorSerializer
from api.views import BookViewSet, AuthorViewSet
from rest_framework.test import APIRequestFactory


class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved1(self):
        url = reverse('books-list')
        self.assertEquals(resolve(url).func.__name__, BookViewSet.__name__)

        url = reverse('author-list')
        self.assertEquals(resolve(url).func.__name__, AuthorViewSet.__name__)


class TestJwt(APITestCase):
    def test_api_jwt(self):
        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        user.is_active = False
        user.save()

        url = reverse('token_obtain_pair')
        resp = self.client.post(
            url, {'username': 'user', 'password': 'pass'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        user.is_active = True
        user.save()

        resp = self.client.post(
            url, {'username': 'user', 'password': 'pass'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class TestBookView(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        self.client.force_authenticate(user=user)

    def test_book_list_get(self):
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_book_post(self):
        author = {
            'name': 'author-test-1',
            'added_by': '1',
        }
        url = reverse('author-list')
        response = self.client.post(url,
                                    data=author, format='json')
        self.assertEquals(response.status_code, 201)

        book = {
            'title': 'book-test-1',
            'author': '1',
            'price': 123,
        }
        url = reverse('books-list')
        response = self.client.post(url,
                                    data=book, format='json')
        self.assertEquals(response.status_code, 201)


class TestAuthorView(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        self.client.force_authenticate(user=user)
        Author.objects.create(
            name='Mehran', added_by=user)

    def test_author_list_get(self):
        url = reverse('author-list')
        response = self.client.get(url)

        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEquals(response.status_code, 200)

    def test_author_list_post(self):
        author = {
            'name': 'author-test-1',
            'added_by': '1',
        }
        url = reverse('author-list')
        response = self.client.post(url,
                                    data=author, format='json')
        self.assertEquals(response.status_code, 201)

    def test_author_list_post_invalid_name(self):
        author = {
            'name': 'author-test@@!@#',
            'added_by': '1',
        }
        url = reverse('author-list')
        response = self.client.post(url,
                                    data=author, format='json')

        self.assertEqual(response.status_code, 400)


class TestBookDelete(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='user@foo.com', password='pass')
        User.objects.create_user(username='mehran', email='user@foo.com', password='mehran')

        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'user', 'password': 'pass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_delete_book_with_user(self):
        author = Author.objects.create(
            name='Mehran', added_by=User.objects.get(username='user'))
        book = Book.objects.create(
            title='Mehran', author=author, price=123)
        url = reverse('books-detail', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_book_with_user_fail_to_delete(self):
        author = Author.objects.create(
            name='Mehran', added_by=User.objects.get(username='mehran'))
        book = Book.objects.create(
            title='Mehran', author=author, price=123)

        url = reverse('books-detail', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)
