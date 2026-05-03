from django.urls import path
from .views import news_detail, news_page

app_name = 'news'

urlpatterns = [
    path('', news_page, name='news_page'),
    path('<int:news_id>/', news_detail, name='news_detail'),
]

