from django.urls import path

from .views import (
    user_register, user_login, user_logout, user_account,
    active_reservs, inactive_reservs, canceled_reservs,
    personal_data
)

app_name = 'accounts'

urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('account/', user_account, name='account'),
    path('active/', active_reservs, name='active_reservs'),
    path('inactive/', inactive_reservs, name='inactive_reservs'),
    path('canceled/', canceled_reservs, name='canceled_reservs'),
    path('personal-data/', personal_data, name='personal_data'),
]