from django.urls import path
from .views import about_page, location_page

app_name = "about"

urlpatterns = [
    path("", about_page, name="about_page"),
    path("location/", location_page, name="location_page"),
]
