from django.urls import path

from .views import *

app_name = 'blogs'

urlpatterns = [
    path('', InterestingPlacesView.as_view(), name='home'),
    path('locality/', LocalitiesView.as_view(), name='localities'),
    path('<str:slug>/', InterestingPlacesDetailView.as_view(), name='place'),
    path('locality/<str:slug>/', LocalitiesDetailView.as_view(), name='locality'),
]