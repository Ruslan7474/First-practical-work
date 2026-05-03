from django.contrib import admin
from .models import News, NewsComment


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at")
    list_filter = ("published_at",)
    search_fields = ("title", "text")
    date_hierarchy = "published_at"
    fields = ("title", ("photo", "photo_url"), "text", "published_at")


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ("news", "user", "parent", "created_at")
    list_filter = ("created_at",)
    search_fields = ("news__title", "user__username", "user__email", "text")
