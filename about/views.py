from collections import OrderedDict
from datetime import date

from django.shortcuts import render
from django.utils import timezone
from theatre.models import HomeShowcaseItem, ShowcaseCategory, ShowTime


def home_page(request):
    query = request.GET.get("q", "").strip()
    today: date = timezone.localdate()

    showcase_items = (
        HomeShowcaseItem.objects.filter(is_active=True, display_date=today)
        .select_related("play")
        .prefetch_related("categories", "play__showtimes", "play__categories")
        .order_by("order", "id")
    )
    if query:
        showcase_items = showcase_items.filter(play__categories__name__icontains=query).distinct()
    showcase_items_exist = showcase_items.exists()

    categories = ShowcaseCategory.objects.filter(is_active=True).order_by("order", "name")

    all_showtimes = (
        ShowTime.objects.filter(starts_at__date__gte=today)
        .select_related("play")
        .prefetch_related("play__categories")
        .order_by("play_id", "hall", "starts_at")
    )
    if query:
        all_showtimes = all_showtimes.filter(play__categories__name__icontains=query).distinct()

    sessions_map: OrderedDict[int, dict] = OrderedDict()
    for st in all_showtimes:
        play_cat_ids = sorted(st.play.categories.values_list("id", flat=True))
        entry = sessions_map.setdefault(
            st.play_id,
            {"play": st.play, "halls": OrderedDict(), "showtimes": [], "cat_ids": play_cat_ids},
        )
        entry["halls"].setdefault(st.hall, []).append(st)
        entry["showtimes"].append(st)

    sessions = []
    for v in sessions_map.values():
        local_dt = [timezone.localtime(st.starts_at) for st in v["showtimes"]]
        dates = sorted({dt.date().isoformat() for dt in local_dt})
        sessions.append(
            {
                "play": v["play"],
                "halls": v["halls"].items(),
                "date_keys": dates,
                "hour_keys": sorted({dt.hour for dt in local_dt}),
                "cat_ids": v["cat_ids"],
            }
        )

    return render(
        request,
        "home.html",
        {
            "showcase_items": showcase_items,
            "showcase_items_exist": showcase_items_exist,
            "categories": categories,
            "sessions": sessions,
            "search_query": query,
        },
    )


def about_page(request):
    return render(request, "about/about_page.html")


def location_page(request):
    # simple static page where an embedded Google Maps link and additional info
    return render(request, "about/location_page.html")
