from django.urls import path

from .views import *

app_name = 'blogs'

urlpatterns = [
    path('', home, name='home'),
    path('places/', InterestingPlacesView.as_view(), name='places'),
    path('locality/', LocalitiesView.as_view(), name='localities'),
    path('<str:slug>/', InterestingPlacesDetailView.as_view(), name='place'),
    path('locality/<str:slug>/', LocalitiesDetailView.as_view(), name='locality'),
]