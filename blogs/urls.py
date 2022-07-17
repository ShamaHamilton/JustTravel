from django.urls import path

from .views import(
    home, localities_view, locality_detail_view,
    places_view, place_detail_view
)

app_name = 'blogs'

urlpatterns = [
    path('', home, name='home'),
    path('places/', places_view, name='places'),
    path('place/<str:slug>/', place_detail_view, name='place'),
    path('localities/', localities_view, name='localities'),
    path('locality/<str:slug>/', locality_detail_view, name='locality'),
]