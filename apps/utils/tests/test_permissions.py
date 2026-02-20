from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory

from apps.utils.permissions.rbac import IsAdmin, IsEditorOrAdmin, IsAnyRole

User = get_user_model()


def make_user(username, group_name=None):
    user = User.objects.create_user(username=username, password="pass", email=f"{username}@test.com")
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


class PermissionTestBase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = make_user("admin_user", "admin")
        self.editor_user = make_user("editor_user", "editor")
        self.viewer_user = make_user("viewer_user", "viewer")
        self.no_group_user = make_user("no_group_user")

    def _has_perm(self, permission, user):
        request = self.factory.get("/")
        request.user = user
        return permission.has_permission(request, view=None)


class IsAdminTests(PermissionTestBase):
    def setUp(self):
        super().setUp()
        self.perm = IsAdmin()

    def test_admin_allowed(self):
        self.assertTrue(self._has_perm(self.perm, self.admin_user))

    def test_editor_denied(self):
        self.assertFalse(self._has_perm(self.perm, self.editor_user))

    def test_viewer_denied(self):
        self.assertFalse(self._has_perm(self.perm, self.viewer_user))

    def test_no_group_denied(self):
        self.assertFalse(self._has_perm(self.perm, self.no_group_user))


class IsEditorOrAdminTests(PermissionTestBase):
    def setUp(self):
        super().setUp()
        self.perm = IsEditorOrAdmin()

    def test_admin_allowed(self):
        self.assertTrue(self._has_perm(self.perm, self.admin_user))

    def test_editor_allowed(self):
        self.assertTrue(self._has_perm(self.perm, self.editor_user))

    def test_viewer_denied(self):
        self.assertFalse(self._has_perm(self.perm, self.viewer_user))

    def test_no_group_denied(self):
        self.assertFalse(self._has_perm(self.perm, self.no_group_user))


class IsAnyRoleTests(PermissionTestBase):
    def setUp(self):
        super().setUp()
        self.perm = IsAnyRole()

    def test_admin_allowed(self):
        self.assertTrue(self._has_perm(self.perm, self.admin_user))

    def test_editor_allowed(self):
        self.assertTrue(self._has_perm(self.perm, self.editor_user))

    def test_viewer_allowed(self):
        self.assertTrue(self._has_perm(self.perm, self.viewer_user))

    def test_no_group_denied(self):
        self.assertFalse(self._has_perm(self.perm, self.no_group_user))
