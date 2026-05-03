from django.urls import path
from .views import afisha_page

app_name = "afisha"

urlpatterns = [
    path("", afisha_page, name="afisha_page"),
]
