from django.db import models


class Performance(models.Model):
    class PerformanceStatus(models.TextChoices):
        REPERTOIRE = "repertoire", "В репертуаре"
        SOON = "soon", "Скоро"
        ARCHIVE = "archive", "Архив"

    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to="performances/posters/")
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Длительность в минутах")
    age_limit = models.CharField(max_length=20)
    director = models.CharField(max_length=255)
    cast = models.TextField()
    premiere_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=PerformanceStatus.choices,
        default=PerformanceStatus.REPERTOIRE,
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
