from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, StudentProfile, ActivityLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "first_name", "last_name", "role", "is_active"]
    list_filter = ["role", "is_active"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profile", {"fields": ("role", "pnfl", "phone", "avatar")}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["student_id", "user", "group", "course", "status", "grant_status"]
    list_filter = ["course", "group", "status", "grant_status"]
    search_fields = ["student_id", "user__first_name", "user__last_name"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "entity_type", "created_at"]
    list_filter = ["action", "entity_type"]
    readonly_fields = ["user", "target_user", "action", "entity_type", "entity_id", "description", "metadata", "created_at"]
