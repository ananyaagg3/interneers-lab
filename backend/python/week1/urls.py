from django.urls import path
from .views import weather_view

urlpatterns = [
    path("week1/", weather_view),
]