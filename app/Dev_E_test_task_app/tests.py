# pylint: skip-file

import json

from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import MyUser

READ_SERIALIZER_FIELDS = ("id", "username", "first_name", "last_name", "is_active", "last_login", "is_superuser")

USER_DATA_WITHOUT_USERNAME = {
    "password": "Password123xxx",
    "is_active": True,
    "first_name": "FName",
    "last_name": "LName",
}
USER_DATA_WITHOUT_PASSWORD = {
    "username": "user1",
    "is_active": True,
    "first_name": "FName",
    "last_name": "LName",
}

GOOD_USER_DATA = {
    "username": "user1",
    "password": "Password123",
    "is_active": True,
    "first_name": "FName",
    "last_name": "LName",
}

USER_DATA_WRONG_PASSWORD = {
    "username": "user3",
    "password": "password",
    "is_active": True,
    "first_name": "FName",
    "last_name": "LName",
}

USER_DATA_WRONG_USERNAME = {
    "username": "user1$",
    "password": "password",
    "is_active": True,
    "first_name": "FName",
    "last_name": "LName",
}


class UserCreateListTestCase(APITestCase):
    url = reverse("Dev_E_test_task_app:user-list")

    def test_failed_user_registration_without_username(self):
        """
        Test to verify that payload with no username is handled
        """
        response = self.client.post(self.url, USER_DATA_WITHOUT_USERNAME)
        self.assertEqual(400, response.status_code)

    def test_failed_user_registration_without_password(self):
        """
        Test to verify that payload with no password is handled
        """
        response = self.client.post(self.url, USER_DATA_WITHOUT_PASSWORD)
        self.assertEqual(400, response.status_code)

    def test_successful_user_registration(self):
        """
        Test with success data
        """
        response = self.client.post(self.url, GOOD_USER_DATA)
        self.assertEqual(201, response.status_code)
        self.assertTrue(all(i in READ_SERIALIZER_FIELDS for i in json.loads(response.content)))

    def test_unique_username_validation(self):
        """
        Test to verify that already exists usernames are forbidden
        """
        user_cred = {
            "username": "user2",
            "password": "Password123",
            "is_active": True,
            "first_name": "FName",
            "last_name": "LName",
        }
        response = self.client.post(self.url, user_cred)
        self.assertEqual(201, response.status_code)

        response = self.client.post(self.url, user_cred)
        self.assertEqual(400, response.status_code)

    def test_user_registration_password_validation(self):
        """
        Test to verify that password validation works
        """
        response = self.client.post(self.url, USER_DATA_WRONG_PASSWORD)
        self.assertEqual(400, response.status_code)

    def test_user_registration_username_validation(self):
        """
        Test to verify that username validation works
        """
        response = self.client.post(self.url, USER_DATA_WRONG_USERNAME)
        self.assertEqual(400, response.status_code)

    def test_get_all_users(self):
        """
        Test getting all users
        """
        for i in range(5):
            MyUser.objects.create_user(f"user{i}", "Password123456")

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(5, len(data))

        for user_info in data:
            self.assertTrue(all(i in READ_SERIALIZER_FIELDS for i in user_info))


class UserAuthTokenTestCase(APITestCase):
    url = reverse("Dev_E_test_task_app:api-token-auth")

    def setUp(self):
        """
        Create a user at setting up test cases
        """
        self.username = "egreth"
        self.password = "Password12345"
        self.user = MyUser.objects.create_user(self.username, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "xxxxxx"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "cczxcxcx"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))


class UserTokenAPIViewTestCase(APITestCase):
    def url(self, pk):
        return reverse("Dev_E_test_task_app:user-detail", kwargs={"pk": pk})

    def setUp(self):
        """
        Create a user at setting up test cases
        """
        self.username = "egreth"
        self.password = "Password12345"
        self.user = MyUser.objects.create_user(self.username, self.password)
        self.token = Token.objects.create(user=self.user)
        self.set_api_authentication_cred(self.token)

        self.user_2 = MyUser.objects.create_user("egreth2", "Password123456")
        self.token_2 = Token.objects.create(user=self.user_2)

        self.super_user = MyUser.objects.create_superuser("egreth3", "Password1234567")
        self.token_su = Token.objects.create(user=self.super_user)

    def tearDown(self):
        """
        Clean up base after test case
        """
        self.user.delete()
        self.token.delete()
        self.user_2.delete()
        self.token_2.delete()
        self.super_user.delete()
        self.token_su.delete()

    def set_api_authentication_cred(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def clean_api_authentication_cred(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

    # Tests for get
    def test_get(self):
        response = self.client.get(self.url(pk=1))
        self.assertEqual(200, response.status_code)
        self.assertTrue(all(i in READ_SERIALIZER_FIELDS for i in json.loads(response.content)))

    # Tests for delete
    def test_delete_by_key(self):
        response = self.client.delete(self.url(self.token.user.id))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_not_yourself(self):
        response = self.client.delete(self.url(self.token_2.user.id))
        self.assertEqual(403, response.status_code)
        self.assertTrue(Token.objects.filter(key=self.token_2.key).exists())

    def test_delete_unauthorized(self):
        self.clean_api_authentication_cred()
        response = self.client.delete(self.url(self.token_2.user.id))
        self.assertEqual(401, response.status_code)
        self.assertTrue(Token.objects.filter(key=self.token_2.key).exists())

    def test_delete_by_superuser(self):
        self.set_api_authentication_cred(self.token_su)
        response = self.client.delete(self.url(self.token_2.user.id))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token_2.key).exists())

    # Tests for put
    def test_put_update_without_username(self):
        response = self.client.put(self.url(self.token.user.id), USER_DATA_WITHOUT_USERNAME)
        self.assertEqual(400, response.status_code)

    def test_put_update_without_password(self):
        response = self.client.put(self.url(self.token.user.id), USER_DATA_WITHOUT_PASSWORD)
        self.assertEqual(400, response.status_code)

    def test_put_update_wrong_username(self):
        response = self.client.put(self.url(self.token.user.id), USER_DATA_WRONG_USERNAME)
        self.assertEqual(400, response.status_code)

    def test_put_update_wrong_password(self):
        response = self.client.put(self.url(self.token.user.id), USER_DATA_WRONG_PASSWORD)
        self.assertEqual(400, response.status_code)

    def test_put_successful(self):
        response = self.client.put(self.url(self.token.user.id), GOOD_USER_DATA)
        self.assertEqual(200, response.status_code)

    def test_put_update_not_yourself(self):
        response = self.client.put(self.url(self.token_2.user.id), GOOD_USER_DATA)
        self.assertEqual(403, response.status_code)

    def test_put_by_superuser(self):
        self.set_api_authentication_cred(self.token_su)
        response = self.client.put(self.url(self.token.user.id), GOOD_USER_DATA)
        self.assertEqual(200, response.status_code)

    # Tests for patch
    def test_patch_update_wrong_password(self):
        response = self.client.patch(self.url(self.token.user.id), USER_DATA_WRONG_PASSWORD)
        self.assertEqual(400, response.status_code)

    def test_patch_successful(self):
        response = self.client.patch(self.url(self.token.user.id), GOOD_USER_DATA)
        self.assertEqual(200, response.status_code)

    def test_patch_update_not_yourself(self):
        response = self.client.patch(self.url(self.token_2.user.id), GOOD_USER_DATA)
        self.assertEqual(403, response.status_code)

    def test_patch_by_superuser(self):
        self.set_api_authentication_cred(self.token_su)
        response = self.client.patch(self.url(self.token.user.id), GOOD_USER_DATA)
        self.assertEqual(200, response.status_code)
