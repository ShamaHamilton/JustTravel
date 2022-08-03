from django import template
from datetime import date
from django.db.models import Q

from rooms.models import Reservation


register = template.Library()


@register.inclusion_tag('accounts/account_header.html', takes_context=True)
def account_header(context):
    request = context['request']
    reservs = Reservation.objects.filter(user=request.user)
    # Активные резервы
    active_reservs = reservs.filter(
        Q(status=True),
        Q(end_date__gte=date.today())
    ).count()
    #  Неактивные резервы
    inactive_reservs = reservs.filter(
        Q(status=True),
        Q(end_date__lt=date.today())
    ).count()
    # Отмененные резервы
    canceled_reservs = reservs.filter(
        Q(status=False)
    ).count()
    context = {
        'active_reservs': active_reservs,
        'inactive_reservs': inactive_reservs,
        'canceled_reservs': canceled_reservs,
    }
    return context
