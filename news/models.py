from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field


class News(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="news/photos/", blank=True, null=True)
    photo_url = models.URLField(blank=True, default="")
    text = CKEditor5Field(config_name="default")
    published_at = models.DateTimeField()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title


class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="news_comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Комментарий к событию"
        verbose_name_plural = "Комментарии к событиям"

    def __str__(self) -> str:
        return f"{self.user} -> {self.news.title}"
