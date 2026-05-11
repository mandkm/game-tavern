from django.urls import reverse
from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

class UserViewTest(TestCase):
    def test_user_list_view(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)