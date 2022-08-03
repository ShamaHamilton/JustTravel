from django import template
from django.db.models import Q
from datetime import date, timedelta

from rooms.models import Reservation

register = template.Library()


@register.inclusion_tag('landlord/landlord_header.html', takes_context=True)
def landlord_header(context):
    request = context['request']
    reservs = Reservation.objects.filter(
        Q(apartment__landlord=request.user),
        Q(status=True)
    )
    # Выезжают
    leaving = reservs.filter(
        Q(start_date__lt=date.today()),
        Q(end_date=date.today()) |
        Q(end_date=date.today() + timedelta(1))
    ).count()
    # Проживают
    reside = reservs.filter(
        Q(start_date__lt=date.today()),
        Q(end_date__gt=date.today())
    ).count()
    # Скоро приедут
    will_arrive_soon = reservs.filter(
        Q(start_date=date.today()) |
        Q(start_date=date.today() + timedelta(1))
    ).count()
    # Предстоящие
    upcoming = reservs.filter(
        Q(start_date__gte=date.today())
    ).count()
    context = {
        'leaving': leaving,
        'reside': reside,
        'will_arrive_soon': will_arrive_soon,
        'upcoming': upcoming,
    }
    return context
