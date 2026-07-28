from django.contrib import admin
from .models import AuthorProfile


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_author",
    )

    list_editable = (
        "is_author",
    )

    search_fields = (
        "user__username",
    )