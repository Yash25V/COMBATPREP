from django.test import TestCase
from .models import User

class UserModelTests(TestCase):
    def test_admin_role(self):
        user = User.objects.create_user(username='admin_test', password='testpassword', role='ADMIN')
        self.assertTrue(user.is_admin())
        self.assertFalse(user.is_officer())
        self.assertFalse(user.is_soldier())

    def test_officer_role(self):
        user = User.objects.create_user(username='officer_test', password='testpassword', role='OFFICER')
        self.assertTrue(user.is_officer())
        self.assertFalse(user.is_admin())
        self.assertFalse(user.is_soldier())

    def test_soldier_role(self):
        user = User.objects.create_user(username='soldier_test', password='testpassword', role='SOLDIER')
        self.assertTrue(user.is_soldier())
        self.assertFalse(user.is_admin())
        self.assertFalse(user.is_officer())

