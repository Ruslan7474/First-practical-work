from django.urls import path
from .views import tickets_page

app_name = 'tickets'

urlpatterns = [
    path('', tickets_page, name='tickets_page'),
]

