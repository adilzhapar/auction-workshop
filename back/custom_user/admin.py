from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "date_of_birth")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = ("email", "first_name", "last_name", "date_of_birth", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "first_name")


admin.site.register(User, CustomUserAdmin)
