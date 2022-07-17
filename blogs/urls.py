from django.urls import path

from .views import(
    home, localities_list_view, locality_detail_view,
    places_list_view, place_detail_view
)

app_name = 'blogs'

urlpatterns = [
    path('', home, name='home'),
    path('places/', places_list_view, name='places'),
    path('place/<str:slug>/', place_detail_view, name='place'),
    path('localities/', localities_list_view, name='localities'),
    path('locality/<str:slug>/', locality_detail_view, name='locality'),
]