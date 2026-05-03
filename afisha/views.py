from datetime import timedelta
from decimal import Decimal

from django.shortcuts import render
from django.utils import timezone

from theatre.models import ShowTime


RU_MONTHS = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def _format_price(value: Decimal) -> str:
    normalized = value.quantize(Decimal("1.00"))
    if normalized == normalized.quantize(Decimal("1")):
        return f"{int(normalized)}"
    return f"{normalized}".replace(".", ",")


def _build_card(showtime: ShowTime, *, archived: bool = False) -> dict:
    starts_local = timezone.localtime(showtime.starts_at)

    return {
        "id": showtime.id,
        "play_id": showtime.play_id,
        "title": showtime.play.title,
        "poster": showtime.play.poster.url if showtime.play.poster else "",
        "poster_url": showtime.play.poster_url,
        "price": _format_price(showtime.price),
        "datetime_label": starts_local.strftime("%d.%m.%Y %H:%M"),
        "archive_label": f"{starts_local.day} {RU_MONTHS[starts_local.month]}",
        "is_archived": archived,
    }


def afisha_page(request):
    query = request.GET.get("q", "").strip()
    now = timezone.now()
    today = timezone.localdate()
    week_end = today + timedelta(days=6 - today.weekday())

    showtimes = ShowTime.objects.select_related("play")
    if query:
        showtimes = showtimes.filter(play__title__icontains=query)
    showtimes = showtimes.order_by("starts_at", "play__title")

    today_cards = []
    week_cards = []
    month_cards = []
    archive_cards = []

    for showtime in showtimes:
        starts_local = timezone.localtime(showtime.starts_at)
        starts_date = starts_local.date()

        if showtime.starts_at < now:
            archive_cards.append(_build_card(showtime, archived=True))
        elif starts_date == today:
            today_cards.append(_build_card(showtime))
        elif today < starts_date <= week_end:
            week_cards.append(_build_card(showtime))
        else:
            month_cards.append(_build_card(showtime))

    sections = [
        {"key": "today", "title": "Сегодня", "items": today_cards},
        {"key": "week", "title": "На этой неделе", "items": week_cards},
        {"key": "month", "title": "В этом месяце и позже", "items": month_cards},
        {"key": "archive", "title": "Архив", "items": list(reversed(archive_cards))},
    ]

    return render(
        request,
        "afisha/afisha_page.html",
        {
            "has_items": any(section["items"] for section in sections),
            "sections": sections,
            "search_query": query,
        },
    )
