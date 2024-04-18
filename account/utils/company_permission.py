from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from account.models import Company


def add_company_admin_permission(user):
    content_type = ContentType.objects.get_for_model(Company)
    permissions = Permission.objects.filter(content_type=content_type)
    for perm in permissions:
        if perm.codename == "company_admin_status":
            user.user_permissions.add(perm)
