from django.urls import path

from .views import MapView, line_notify, ListCountryView

app_name = "notify"

urlpatterns = [
    path("notify/", line_notify, name='notify'),
    path("map/", MapView.as_view()),
    path("get_cities_list/", ListCountryView.as_view())
]