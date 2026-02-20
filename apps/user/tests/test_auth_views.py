from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

LOGIN_URL = "/api/auth/login/"
REFRESH_URL = "/api/auth/token/refresh/"
LOGOUT_URL = "/api/auth/logout/"


def make_user(username, password="testpass123"):
    return User.objects.create_user(username=username, password=password, email=f"{username}@test.com")


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = make_user("login_user")
        self.client = APIClient()

    def test_login_success(self):
        response = self.client.post(LOGIN_URL, {"username": "login_user", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("access", data["data"])
        self.assertIn("refresh", data["data"])
        self.assertEqual(data["data"]["user"]["username"], "login_user")

    def test_login_wrong_password(self):
        response = self.client.post(LOGIN_URL, {"username": "login_user", "password": "wrongpass"})
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json()["success"])

    def test_login_nonexistent_user(self):
        response = self.client.post(LOGIN_URL, {"username": "ghost", "password": "any"})
        self.assertEqual(response.status_code, 401)

    def test_login_missing_username(self):
        response = self.client.post(LOGIN_URL, {"password": "testpass123"})
        self.assertEqual(response.status_code, 400)

    def test_login_missing_password(self):
        response = self.client.post(LOGIN_URL, {"username": "login_user"})
        self.assertEqual(response.status_code, 400)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(LOGIN_URL, {"username": "login_user", "password": "testpass123"})
        self.assertEqual(response.status_code, 401)


class RefreshTokenViewTests(APITestCase):
    def setUp(self):
        self.user = make_user("refresh_user")
        self.refresh_token, _ = get_tokens(self.user)
        self.client = APIClient()

    def test_refresh_success(self):
        response = self.client.post(REFRESH_URL, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json()["data"])

    def test_refresh_invalid_token(self):
        response = self.client.post(REFRESH_URL, {"refresh": "not.a.valid.token"})
        self.assertEqual(response.status_code, 401)

    def test_refresh_missing_token(self):
        response = self.client.post(REFRESH_URL, {})
        self.assertEqual(response.status_code, 400)


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = make_user("logout_user")
        self.refresh_token, self.access_token = get_tokens(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_logout_success(self):
        response = self.client.post(LOGOUT_URL, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    def test_logout_blacklisted_token_rejected(self):
        self.client.post(LOGOUT_URL, {"refresh": self.refresh_token})
        response = self.client.post(LOGOUT_URL, {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, 401)

    def test_logout_invalid_token(self):
        response = self.client.post(LOGOUT_URL, {"refresh": "bad.token.value"})
        self.assertEqual(response.status_code, 401)

    def test_logout_missing_token(self):
        response = self.client.post(LOGOUT_URL, {})
        self.assertEqual(response.status_code, 400)
