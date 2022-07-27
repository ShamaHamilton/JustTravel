from django.urls import path

from .views import (
    CreateRoomView, RoomsView, RoomDetailView, room_reser_details, AddReserv,
    AddStarRating, AddReview, Search
)

app_name = 'rooms'

urlpatterns = [
    path('', RoomsView.as_view(), name='rooms'),
    path('search/', Search.as_view(), name='search'),
    path('add-room/', CreateRoomView.as_view(), name='create_room'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('add-reserv/<int:pk>/', AddReserv.as_view(), name='add_reserv'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('reserv/<int:pk>/', room_reser_details, name='room_reserv_details'),
]