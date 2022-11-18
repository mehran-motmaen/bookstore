from django.test import TestCase

# Create your tests here.
from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from django.test import SimpleTestCase, Client
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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


class TestAuthorView(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        self.client.force_authenticate(user=user)

    def test_author_list_get(self):
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
