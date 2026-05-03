from django.db import models


class Hall(models.Model):
    class HallType(models.TextChoices):
        MAIN = "main", "Основной"
        SMALL = "small", "Малый"
        VIP = "vip", "VIP"

    name = models.CharField(max_length=120)
    seats_count = models.IntegerField()
    scheme = models.JSONField(default=dict, blank=True)
    type = models.CharField(max_length=20, choices=HallType.choices, default=HallType.MAIN)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Session(models.Model):
    class SessionStatus(models.TextChoices):
        ACTIVE = "active", "Активен"
        CANCELED = "canceled", "Отменен"

    performance = models.ForeignKey(
        "afisha.Performance",
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    date = models.DateField()
    time = models.TimeField()
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name="sessions")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.ACTIVE,
    )

    class Meta:
        ordering = ["date", "time"]

    def __str__(self) -> str:
        return f"{self.performance.title} - {self.date} {self.time}"


class Ticket(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Ожидает оплаты"
        PAID = "paid", "Оплачен"

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="tickets")
    seats = models.JSONField(default=list, blank=True)
    buyer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    qr_code = models.ImageField(upload_to="tickets/qr_codes/", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.buyer_name} - {self.session}"
