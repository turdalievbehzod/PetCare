from django.contrib import admin

from apps.users.models.permissions import Role, Endpoint, Permission
from apps.users.models.user_permissions import UserPermission
from apps.users.models.users import User

# --- Remove noisy third-party admin panels ---
# simplejwt token blacklist (internal mechanism — not useful in admin UI)
try:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
    admin.site.unregister(OutstandingToken)
    admin.site.unregister(BlacklistedToken)
except Exception:
    pass

# django-celery-results (internal task result storage)
try:
    from django_celery_results.models import TaskResult, GroupResult
    admin.site.unregister(TaskResult)
    admin.site.unregister(GroupResult)
except Exception:
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'parent', 'created_at']
    search_fields = ['name', 'codename']
    list_filter = ['parent']
    ordering = ['-id']


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ['path', 'method', 'name', 'permission', 'is_active']
    search_fields = ['path', 'name']
    list_filter = ['method', 'is_active', 'permission']
    list_editable = ['is_active']
    ordering = ['-path']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['permissions']
    list_filter = ['is_active']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff']
    search_fields = ['username', 'email']
    filter_horizontal = ['roles']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission', 'created_at']
    search_fields = ['id']
    list_filter = ['created_at']
    ordering = ['-id']