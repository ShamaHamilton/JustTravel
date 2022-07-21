from django.urls import path

from .views import (
    CreateRoomView, RoomsView, room_detail_view, room_reser_details,
    AddStarRating, AddReview
)

app_name = 'rooms'

urlpatterns = [
    path('', RoomsView.as_view(), name='rooms'),
    path('add-room/', CreateRoomView.as_view(), name='create_room'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    # path('<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('<int:pk>/', room_detail_view, name='room_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('rooms/reserv/<int:pk>/', room_reser_details, name='room_reserv_details'),
]