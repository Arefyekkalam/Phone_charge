from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("mobile", "user_type", "is_active",)
    list_filter = ("mobile", "user_type", "is_active",)
    fieldsets = (
        (None, {"fields": ("mobile", "password")}),
        ("Permissions", {"fields": ("user_type","is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "mobile", "password1", "password2", "is_staff", "user_type",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("mobile",)
    ordering = ("mobile",)


admin.site.register(CustomUser, CustomUserAdmin)
