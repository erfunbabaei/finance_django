from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status


class CoreAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register_api")
        self.login_url = reverse("login_api")
        self.dashboard_url = reverse("dashboard_api")
        self.incomes_url = reverse("income-list")
        self.expenses_url = reverse("expense-list")

        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }

    def test_homepage_status_code(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 301, 302, 401, 404])

    def test_app_is_installed(self):
        from django.apps import apps
        self.assertTrue(apps.is_installed("core"))

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_existing_user_fails(self):
        User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        User.objects.create_user(username="testuser", password="testpass123")
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpass123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_dashboard_requires_auth(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_with_auth(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_income", response.data)
        self.assertIn("total_expense", response.data)

    def test_create_income(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.incomes_url, {"title": "Salary", "amount": 5000, "date": "2025-09-15"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_expense(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.expenses_url, {"title": "Groceries", "amount": 200, "date": "2025-09-15"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
