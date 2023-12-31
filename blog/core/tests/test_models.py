"""
Tests for Model
"""
# from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
# from core import models


def create_user(email='user@example.com', password='test123'):
    """
    Create and return a new user
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """
    Test Model Class
    """

    def test_create_user_with_email_successful(self):
        """
        Test Creating a user with an email is successful
        """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test Email is Normalize for new users
        """
        sampleEmails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@EXAMPLE.COM', 'test2@example.com'],
            ['Test3@example.COM', 'Test3@example.com'],
            ['test4@Example.COM', 'test4@example.com'],
            ]
        for email, expectedEmail in sampleEmails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expectedEmail)

    def test_new_user_without_email_raise_error(self):
        """
        Test that creating a user without an email will raise a Value Error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')
