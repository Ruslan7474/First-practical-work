from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0009_alter_showcasecategory_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SeatReservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("row_number", models.PositiveIntegerField(verbose_name="Ряд")),
                ("seat_number", models.PositiveIntegerField(verbose_name="Место")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("showtime", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="seat_reservations", to="theatre.showtime")),
            ],
            options={
                "verbose_name": "Занятое место",
                "verbose_name_plural": "Занятые места",
                "ordering": ["showtime", "row_number", "seat_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="seatreservation",
            constraint=models.UniqueConstraint(fields=("showtime", "row_number", "seat_number"), name="unique_seat_per_showtime"),
        ),
    ]
