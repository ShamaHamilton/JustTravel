from django.urls import path

from .views import (
    CreateRoomView, RoomsView, room_reservation, room_reser_details
)

app_name = 'rooms'

urlpatterns = [
    path('rooms/', RoomsView.as_view(), name='rooms'),
    path('roomadd/', CreateRoomView.as_view(), name='create_room'),
    path('rooms/<int:pk>/', room_reservation, name='room_detail'),
    path('rooms/reserv/<int:pk>/', room_reser_details, name='room_reserv_details'),
]