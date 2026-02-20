from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.records.models.records_model import DataRecord

User = get_user_model()

LIST_URL = "/api/records/"
CREATE_URL = "/api/records/create/"


def detail_url(pk):
    return f"/api/records/{pk}/"


def update_url(pk):
    return f"/api/records/{pk}/update/"


def delete_url(pk):
    return f"/api/records/{pk}/delete/"


def make_user(username, group_name=None):
    user = User.objects.create_user(username=username, password="pass", email=f"{username}@test.com")
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client


class RecordViewTestBase(APITestCase):
    def setUp(self):
        self.admin = make_user("admin_user", "admin")
        self.editor = make_user("editor_user", "editor")
        self.viewer = make_user("viewer_user", "viewer")
        self.no_role = make_user("no_role_user")

        self.admin_client = auth_client(self.admin)
        self.editor_client = auth_client(self.editor)
        self.viewer_client = auth_client(self.viewer)
        self.no_role_client = auth_client(self.no_role)
        self.anon_client = APIClient()

        self.record = DataRecord.objects.create(title="Test Record", description="desc", is_active=True)


class RecordListViewTests(RecordViewTestBase):
    def test_admin_can_list(self):
        response = self.admin_client.get(LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_editor_can_list(self):
        response = self.editor_client.get(LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_viewer_can_list(self):
        response = self.viewer_client.get(LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_no_role_denied(self):
        response = self.no_role_client.get(LIST_URL)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_denied(self):
        response = self.anon_client.get(LIST_URL)
        self.assertEqual(response.status_code, 401)

    def test_list_returns_paginated_results(self):
        response = self.admin_client.get(LIST_URL)
        data = response.json()["data"]
        self.assertIn("results", data)
        self.assertIn("count", data)

    def test_search_filter(self):
        DataRecord.objects.create(title="Unique Title XYZ", is_active=True)
        response = self.admin_client.get(LIST_URL, {"search": "XYZ"})
        results = response.json()["data"]["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Unique Title XYZ")


class RecordCreateViewTests(RecordViewTestBase):
    def _payload(self, title="New Record"):
        return {"title": title, "description": "some desc", "is_active": True}

    def test_admin_can_create(self):
        response = self.admin_client.post(CREATE_URL, self._payload("Admin Record"))
        self.assertEqual(response.status_code, 201)

    def test_editor_can_create(self):
        response = self.editor_client.post(CREATE_URL, self._payload("Editor Record"))
        self.assertEqual(response.status_code, 201)

    def test_viewer_denied(self):
        response = self.viewer_client.post(CREATE_URL, self._payload())
        self.assertEqual(response.status_code, 403)

    def test_no_role_denied(self):
        response = self.no_role_client.post(CREATE_URL, self._payload())
        self.assertEqual(response.status_code, 403)

    def test_anonymous_denied(self):
        response = self.anon_client.post(CREATE_URL, self._payload())
        self.assertEqual(response.status_code, 401)

    def test_missing_title_returns_400(self):
        response = self.admin_client.post(CREATE_URL, {"description": "no title"})
        self.assertEqual(response.status_code, 400)


class RecordRetrieveViewTests(RecordViewTestBase):
    def test_admin_can_retrieve(self):
        response = self.admin_client.get(detail_url(self.record.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["id"], self.record.pk)

    def test_editor_can_retrieve(self):
        response = self.editor_client.get(detail_url(self.record.pk))
        self.assertEqual(response.status_code, 200)

    def test_viewer_can_retrieve(self):
        response = self.viewer_client.get(detail_url(self.record.pk))
        self.assertEqual(response.status_code, 200)

    def test_no_role_denied(self):
        response = self.no_role_client.get(detail_url(self.record.pk))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_denied(self):
        response = self.anon_client.get(detail_url(self.record.pk))
        self.assertEqual(response.status_code, 401)

    def test_not_found(self):
        response = self.admin_client.get(detail_url(9999))
        self.assertEqual(response.status_code, 404)


class RecordUpdateViewTests(RecordViewTestBase):
    def test_admin_can_update(self):
        response = self.admin_client.patch(update_url(self.record.pk), {"title": "Updated by Admin"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], "Updated by Admin")

    def test_editor_can_update(self):
        response = self.editor_client.patch(update_url(self.record.pk), {"title": "Updated by Editor"})
        self.assertEqual(response.status_code, 200)

    def test_viewer_denied(self):
        response = self.viewer_client.patch(update_url(self.record.pk), {"title": "Viewer attempt"})
        self.assertEqual(response.status_code, 403)

    def test_no_role_denied(self):
        response = self.no_role_client.patch(update_url(self.record.pk), {"title": "No role attempt"})
        self.assertEqual(response.status_code, 403)

    def test_anonymous_denied(self):
        response = self.anon_client.patch(update_url(self.record.pk), {"title": "Anon attempt"})
        self.assertEqual(response.status_code, 401)

    def test_not_found(self):
        response = self.admin_client.patch(update_url(9999), {"title": "Ghost"})
        self.assertEqual(response.status_code, 404)


class RecordDeleteViewTests(RecordViewTestBase):
    def test_admin_can_delete(self):
        response = self.admin_client.delete(delete_url(self.record.pk))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(DataRecord.objects.filter(pk=self.record.pk).exists())

    def test_editor_denied(self):
        response = self.editor_client.delete(delete_url(self.record.pk))
        self.assertEqual(response.status_code, 403)

    def test_viewer_denied(self):
        response = self.viewer_client.delete(delete_url(self.record.pk))
        self.assertEqual(response.status_code, 403)

    def test_no_role_denied(self):
        response = self.no_role_client.delete(delete_url(self.record.pk))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_denied(self):
        response = self.anon_client.delete(delete_url(self.record.pk))
        self.assertEqual(response.status_code, 401)

    def test_not_found(self):
        response = self.admin_client.delete(delete_url(9999))
        self.assertEqual(response.status_code, 404)
