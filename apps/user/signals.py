from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


GROUP_PERMISSIONS = {
    "admin":  ["add_datarecord", "change_datarecord", "delete_datarecord", "view_datarecord"],
    "editor": ["add_datarecord", "change_datarecord", "view_datarecord"],
    "viewer": ["view_datarecord"],
}


@receiver(post_migrate)
def create_role_groups(sender, **kwargs):
    try:
        from apps.records.models.records_model import DataRecord
        content_type = ContentType.objects.get_for_model(DataRecord)
    except Exception:
        return

    for group_name, codenames in GROUP_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=codenames,
        )
        group.permissions.set(perms)
