from django.urls import path

from .views import (
    user_register, user_login, user_logout, user_account,
    user_active_reservs, user_inactive_reservs, user_canceled_reservs,
    landlord_leaving, landlord_reside, landlord_will_arrive_soon, landlord_upcoming
)

app_name = 'accounts'

urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('account/', user_account, name='account'),
    path('active/', user_active_reservs, name='user_active_reservs'),
    path('inactive/', user_inactive_reservs, name='user_inactive_reservs'),
    path('canceled/', user_canceled_reservs, name='user_canceled_reservs'),
    path('leaving/', landlord_leaving, name='landlord_leaving'),
    path('reside/', landlord_reside, name='landlord_reside'),
    path('will_arrive_soon/', landlord_will_arrive_soon, name='landlord_will_arrive_soon'),
    path('upcoming/', landlord_upcoming, name='landlord_upcoming'),
]