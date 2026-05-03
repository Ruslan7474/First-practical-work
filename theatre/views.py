import json

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from .models import HALL_BIG, Play, SeatReservation, ShowTime


def _has_meaningful_description(html: str | None) -> bool:
    text = strip_tags(html or "")
    text = text.replace("\xa0", " ").replace("&nbsp;", " ").strip()
    return bool(text)


def _hall_size(hall_name: str) -> int:
    return 16 if hall_name == HALL_BIG else 10


def home(request):
    plays = (
        Play.objects.prefetch_related("showtimes", "categories")
        .filter(showtimes__starts_at__gte=timezone.now())
        .distinct()
    )
    return render(request, "theatre/home.html", {"plays": plays})


def play_detail(request, play_id):
    play = get_object_or_404(
        Play.objects.prefetch_related("categories", "showtimes__seat_reservations"),
        pk=play_id,
    )
    upcoming_showtimes = list(play.showtimes.filter(starts_at__gte=timezone.now()).order_by("starts_at"))
    booking_showtimes = upcoming_showtimes or list(play.showtimes.all().order_by("starts_at"))

    seat_maps = [
        {
            "id": show.id,
            "label": timezone.localtime(show.starts_at).strftime("%d.%m.%Y %H:%M"),
            "price": str(show.price) if show.price is not None else "",
            "hall": show.hall,
            "size": _hall_size(show.hall),
            "reserved": [
                {"row": seat.row_number, "seat": seat.seat_number}
                for seat in show.seat_reservations.all()
            ],
        }
        for show in booking_showtimes
    ]

    return render(
        request,
        "theatre/play_detail.html",
        {
            "play": play,
            "play_description_html": play.description if _has_meaningful_description(play.description) else "",
            "upcoming_showtimes": booking_showtimes,
            "has_real_upcoming_showtimes": bool(upcoming_showtimes),
            "seat_maps": seat_maps,
        },
    )


@require_POST
def reserve_seats(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "invalid_payload"}, status=400)

    seats = payload.get("seats") or []
    hall_size = _hall_size(showtime.hall)
    normalized = []

    for seat in seats:
        try:
            row_number = int(seat["row"])
            seat_number = int(seat["seat"])
        except (KeyError, TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "invalid_seat"}, status=400)

        if not (1 <= row_number <= hall_size and 1 <= seat_number <= hall_size):
            return JsonResponse({"ok": False, "error": "seat_out_of_range"}, status=400)

        normalized.append((row_number, seat_number))

    normalized = list(dict.fromkeys(normalized))
    if not normalized:
        return JsonResponse({"ok": False, "error": "no_seats_selected"}, status=400)

    existing = set(
        showtime.seat_reservations.values_list("row_number", "seat_number")
    )
    conflicts = [seat for seat in normalized if seat in existing]
    if conflicts:
        return JsonResponse(
            {
                "ok": False,
                "error": "seats_already_reserved",
                "conflicts": [{"row": row, "seat": seat} for row, seat in conflicts],
            },
            status=409,
        )

    try:
        with transaction.atomic():
            SeatReservation.objects.bulk_create(
                [
                    SeatReservation(showtime=showtime, row_number=row, seat_number=seat)
                    for row, seat in normalized
                ]
            )
    except IntegrityError:
        return JsonResponse({"ok": False, "error": "seats_already_reserved"}, status=409)

    return JsonResponse(
        {
            "ok": True,
            "reserved": [{"row": row, "seat": seat} for row, seat in normalized],
        }
    )


def booking_success(request, play_id):
    play = get_object_or_404(Play, pk=play_id)
    return render(request, "theatre/booking_success.html", {"play": play})
