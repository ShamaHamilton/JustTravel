from django import template
from datetime import date, timedelta

from rooms.models import RoomsApplicationModel, Reservation

register = template.Library()


@register.inclusion_tag('landlord/landlord_nav.html', takes_context=True)
def landlord_nav(context):
    request = context['request']
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    leaving = []
    reside = []
    will_arrive_soon = []
    upcoming = []
    if landlord_apartments:
        for apartment in landlord_apartments:
            apartment_reservs = Reservation.objects.filter(
                apartment_id=apartment.pk
            )
            if apartment_reservs:
                for reserv in apartment_reservs:
                    # Выезжают
                    if (reserv.end_date == date.today() or
                        reserv.end_date == date.today() + timedelta(1) and
                        reserv.start_date < date.today()):
                        leaving.append(reserv)
                    # Проживают
                    elif(reserv.start_date < date.today() and
                         reserv.end_date > date.today() + timedelta(1)):
                        reside.append(reserv)
                    # Скоро приедут
                    elif(reserv.start_date == date.today() or
                         reserv.start_date == date.today() + timedelta(1)):
                        will_arrive_soon.append(reserv)
                    # Предстоящие
                    elif (reserv.start_date > date.today() + timedelta(1)):
                        upcoming.append(reserv)
    context = {
        'leaving': leaving,
        'reside': reside,
        'will_arrive_soon': will_arrive_soon,
        'upcoming': upcoming,
    }
    return context
