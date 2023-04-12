from django.urls import path

from .views import MapView, line_notify, ListCountryView, UploadFileViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include

app_name = "notify"

router = DefaultRouter()
router.register(r'get_cities_list', ListCountryView, basename='get_cities_list')

urlpatterns = [
    path("notify/", line_notify, name='notify'),
    path("map/", MapView.as_view()),
    path("api/",  include(router.urls)),
    path("upload/", UploadFileViewSet.as_view())
]