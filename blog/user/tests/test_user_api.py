from django.test import TestCase
from graphene.test import Client 
from core.models import User
from ..schema import schema
from rest_framework.test import APIClient


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com",
        }

    def test_user_signup(self):
        mutation = '''
            mutation {
                CreateUser(input: {
                    username: "testuser",
                    password1: "testpassword",
                    email: "testuser@example.com",
                }) {
                    user {
                        id
                        username
                        email
                    }
                }
            }
        '''

        response = self.client.execute(mutation)
        data = response.get('data', {})
        # print(data)
        user = data.get('CreateUser', {}).get('user', {})
        # .get('user', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['email'], "testuser@example.com")

    def test_edit_user_details(self):
        # Create a user to edit
        user = User.objects.create_user(
            username="edituser",
            password="editpassword",
            email="edituser@example.com",
        )

        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(self.user_data)
        # self.client.force_login(email="edituser@example.com",
        #                         password="editpassword")
        self.client = Client(schema)
        mutation = '''
            mutation {
                UpdateUser(input: {
                    username: "Edited",
                }) {
                    user {
                        id
                        username
                    }
                }
            }
        '''

        response = self.client.execute(mutation)
        data = response.get('data', {})
        # print(data)
        user = data.get('UpdateUser', {}).get('user', {})
        # .get('user', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(user)
        self.assertEqual(user['username'], "Edited")
