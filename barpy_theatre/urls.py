from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from about.views import home_page
from theatre.views import booking_success, play_detail, reserve_seats

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", home_page, name="home"),
    path("plays/<int:play_id>/", play_detail, name="play_detail"),
    path("plays/<int:play_id>/success/", booking_success, name="booking_success"),
    path("showtimes/<int:showtime_id>/reserve-seats/", reserve_seats, name="reserve_seats"),
    path("afisha/", include("afisha.urls")),
    path("news/", include("news.urls")),
    path("about/", include("about.urls")),
    path("tickets/", include("tickets.urls")),
    path("accounts/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
