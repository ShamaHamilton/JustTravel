from multiprocessing import context
from django import template
from datetime import date, timedelta

from rooms.models import Reservation, RoomsApplicationModel

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


def get_landlord_list(request):
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
                    elif (reserv.start_date < date.today() and 
                        reserv.end_date > date.today() + timedelta(1)):
                        reside.append(reserv)
                    # Скоро приедут
                    elif (reserv.start_date == date.today() or 
                        reserv.start_date == date.today() + timedelta(1)):
                        will_arrive_soon.append(reserv)
                    # Предстоящие
                    elif (reserv.start_date > date.today() + timedelta(1)):
                        upcoming.append(reserv)
    context = {
        'landlord_apartments': landlord_apartments,
        'apartment_reservs': apartment_reservs,
        'leaving': leaving,
        'reside': reside,
        'will_arrive_soon': will_arrive_soon,
        'upcoming': upcoming,
    }
    return context
