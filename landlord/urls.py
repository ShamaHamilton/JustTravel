from django.urls import path

from landlord.views import (
    account, leaving, reside, will_arrive_soon, upcoming
)

app_name = 'landlord'

urlpatterns = [
    path('account/', account, name='account'),
    path('leaving/', leaving, name='leaving'),
    path('reside/', reside, name='reside'),
    path('will_arrive_soon/', will_arrive_soon, name='will_arrive_soon'),
    path('upcoming/', upcoming, name='upcoming'),
]