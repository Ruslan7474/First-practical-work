from django.urls import path
from . import views

app_name = "theatre"

urlpatterns = [
    path("", views.home, name="home"),
    path("plays/<int:play_id>/", views.play_detail, name="play_detail"),
    path("plays/<int:play_id>/success/", views.booking_success, name="booking_success"),
    path("showtimes/<int:showtime_id>/reserve-seats/", views.reserve_seats, name="reserve_seats"),
]
