from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


HALL_UNDEFINED = "Не определен"
HALL_BIG = "Большой зал"
HALL_SMALL = "Маленький зал"
HALL_CHOICES = [
    (HALL_UNDEFINED, HALL_UNDEFINED),
    (HALL_BIG, HALL_BIG),
    (HALL_SMALL, HALL_SMALL),
]


class Play(models.Model):
    title = models.CharField("Название", max_length=200)
    description = CKEditor5Field("Описание", config_name="default")
    poster = models.ImageField("Постер", upload_to="posters/", blank=True, null=True)
    poster_url = models.URLField("Ссылка на постер", blank=True, default="")
    categories = models.ManyToManyField(
        "ShowcaseCategory",
        blank=True,
        related_name="plays",
        verbose_name="Категории",
    )
    genre = models.CharField("Жанр (устаревшее)", max_length=120, blank=True, default="")
    duration_minutes = models.PositiveIntegerField("Длительность (мин.)", blank=True, null=True)
    age_limit = models.CharField("Возрастное ограничение", max_length=10, default="12+")
    director = models.CharField("Режиссер", max_length=160, blank=True, default="")
    cast = models.TextField("Труппа", blank=True, default="")
    premiere_date = models.DateField("Дата премьеры", blank=True, null=True)
    hall = models.CharField("Зал", max_length=120, choices=HALL_CHOICES, default=HALL_UNDEFINED, blank=True)
    status = models.CharField(
        "Статус (устаревшее)",
        max_length=20,
        choices=[
            ("repertory", "В репертуаре"),
            ("soon", "Скоро"),
            ("archive", "Архив"),
        ],
        default="repertory",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Спектакль"
        verbose_name_plural = "Спектакли"

    def __str__(self) -> str:
        return self.title

    def categories_label(self) -> str:
        names = list(self.categories.values_list("name", flat=True))
        return ", ".join(names) if names else "—"


class ShowTime(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="showtimes")
    starts_at = models.DateTimeField("Дата и время начала")
    hall = models.CharField("Зал", max_length=120, choices=HALL_CHOICES, default=HALL_UNDEFINED, blank=True)
    price = models.DecimalField("Цена билета", max_digits=8, decimal_places=2, blank=True, null=True)
    total_seats = models.PositiveIntegerField("Всего мест", default=120)

    class Meta:
        ordering = ["starts_at"]
        verbose_name = "Показ"
        verbose_name_plural = "Показы"

    def __str__(self) -> str:
        return f"{self.play.title} - {self.starts_at:%d.%m.%Y %H:%M}"

    @property
    def hall_capacity(self) -> int:
        if self.hall == HALL_BIG:
            return 16 * 16
        if self.hall == HALL_SMALL:
            return 10 * 10
        return self.total_seats

    @property
    def sold_seats(self) -> int:
        return self.seat_reservations.count() + sum(self.bookings.values_list("seats", flat=True))

    @property
    def available_seats(self) -> int:
        return max(self.hall_capacity - self.sold_seats, 0)

    @property
    def is_upcoming(self) -> bool:
        return self.starts_at >= timezone.now()


class Booking(models.Model):
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name="bookings")
    customer_name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email", blank=True)
    seats = models.PositiveIntegerField("Количество билетов", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self) -> str:
        return f"{self.customer_name} - {self.showtime} ({self.seats})"


class SeatReservation(models.Model):
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name="seat_reservations")
    row_number = models.PositiveIntegerField("Ряд")
    seat_number = models.PositiveIntegerField("Место")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["showtime", "row_number", "seat_number"]
        verbose_name = "Занятое место"
        verbose_name_plural = "Занятые места"
        constraints = [
            models.UniqueConstraint(
                fields=("showtime", "row_number", "seat_number"),
                name="unique_seat_per_showtime",
            )
        ]

    def __str__(self) -> str:
        return f"{self.showtime} - ряд {self.row_number}, место {self.seat_number}"


class ShowcaseCategory(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Категория спектаклей"
        verbose_name_plural = "Категории спектаклей"

    def __str__(self) -> str:
        return self.name


class HomeShowcaseItem(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="home_showcase_items", verbose_name="Спектакль")
    image = models.ImageField("Картинка в карусели", upload_to="home_showcase/", blank=True, null=True)
    image_url = models.URLField("Ссылка на картинку", blank=True, default="")
    categories = models.ManyToManyField(
        ShowcaseCategory,
        blank=True,
        related_name="showcase_items",
        verbose_name="Категории",
    )
    display_date = models.DateField(
        "Дата показа",
        blank=True,
        null=True,
        help_text="Если указать дату, карточка покажется только в этот день. Если пусто, карточка считается общей.",
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Карточка витрины на главной"
        verbose_name_plural = "Карточки витрины на главной"

    def __str__(self) -> str:
        date_label = self.display_date.strftime("%d.%m.%Y") if self.display_date else "без даты"
        return f"{self.play.title} ({date_label})"

    @classmethod
    def get_for_home(cls):
        today = timezone.localdate()
        dated = cls.objects.filter(is_active=True, display_date=today).select_related("play")
        if dated.exists():
            return dated.order_by("order", "id")

        common = cls.objects.filter(is_active=True, display_date__isnull=True).select_related("play")
        if common.exists():
            return common.order_by("order", "id")

        return cls.objects.filter(is_active=True).select_related("play").order_by("order", "id")
