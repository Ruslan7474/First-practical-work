from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0007_play_hall_alter_showtime_hall"),
    ]

    operations = [
        migrations.AddField(
            model_name="play",
            name="poster_url",
            field=models.URLField(blank=True, default="", verbose_name="Poster URL"),
        ),
    ]
