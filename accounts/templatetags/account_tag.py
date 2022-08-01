from django import template
from datetime import date
from django.db.models import Q

from rooms.models import Reservation


register = template.Library()


@register.inclusion_tag('accounts/account_header.html', takes_context=True)
def account_header(context):
    request = context['request']
    reservs = Reservation.objects.filter(user_id=request.user)
    active_reservs = []
    inactive_reservs = []
    canceled_reservs = []
    for reserv in reservs:
        if reserv.end_date >= date.today() and reserv.status:
            active_reservs.append(reserv)
        elif reserv.status == False:
            canceled_reservs.append(reserv)
        else:
            inactive_reservs.append(reserv)
    context = {
        'active_reservs': active_reservs,
        'inactive_reservs': inactive_reservs,
        'canceled_reservs': canceled_reservs,
    }
    return context
