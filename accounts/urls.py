from django.urls import path

from .views import (
    CreateUserView, LoginView, user_login, user_logout
)

app_name = 'accounts'

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]