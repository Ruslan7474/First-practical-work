from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0010_seatreservation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="play",
            name="director",
            field=models.CharField(blank=True, default="", max_length=160, verbose_name="Режиссер"),
        ),
        migrations.AlterField(
            model_name="play",
            name="duration_minutes",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Длительность (мин.)"),
        ),
        migrations.AlterField(
            model_name="play",
            name="hall",
            field=models.CharField(blank=True, choices=[("Не определен", "Не определен"), ("Большой зал", "Большой зал"), ("Маленький зал", "Маленький зал")], default="Не определен", max_length=120, verbose_name="Зал"),
        ),
        migrations.AlterField(
            model_name="showtime",
            name="hall",
            field=models.CharField(blank=True, choices=[("Не определен", "Не определен"), ("Большой зал", "Большой зал"), ("Маленький зал", "Маленький зал")], default="Не определен", max_length=120, verbose_name="Зал"),
        ),
        migrations.AlterField(
            model_name="showtime",
            name="price",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name="Цена билета"),
        ),
    ]
