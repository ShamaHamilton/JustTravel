from django import template
from datetime import date

from rooms.models import Reservation

register = template.Library()


def get_reservs_list(request):
    user_reservs = Reservation.objects.filter(name_reserv_id=request.user)
    active_reservs = []
    inactive_reservs = []
    canceled_reservs = []
    for user_reserv in user_reservs:
        if user_reserv.end_date >= date.today() and user_reserv.status:
            active_reservs.append(user_reserv)
        elif user_reserv.status == False:
            canceled_reservs.append(user_reserv)
        else:
            inactive_reservs.append(user_reserv)
    context = {
        'active_reservs': active_reservs,
        'inactive_reservs': inactive_reservs,
        'canceled_reservs': canceled_reservs,
    }
    return context