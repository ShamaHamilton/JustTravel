from django.shortcuts import render
from django.db.models import Q

from datetime import date, timedelta

from accounts.models import CustomUser
from rooms.models import RoomsApplicationModel, Reservation

def account(request):
    return render(request, 'landlord/account.html')


def leaving(request):
    """Выезжают."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    leaving = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.end_date == date.today() or
                reserv.end_date == date.today() + timedelta(1) and
                reserv.start_date < date.today()):
                leaving.append(reserv)
    context = {'leaving': leaving}
    return render(request, 'landlord/leaving.html', context)


def reside(request):
    """Проживают."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    reside = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.start_date < date.today() and
                reserv.end_date > date.today() + timedelta(1)):
                reside.append(reserv)
    context = {'reside': reside}
    return render(request, 'landlord/reside.html', context)


def will_arrive_soon(request):
    """Скоро приедут."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    will_arrive_soon = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.start_date == date.today() or
                reserv.start_date == date.today() + timedelta(1)):
                will_arrive_soon.append(reserv)
    context = {'will_arrive_soon': will_arrive_soon}
    return render(request, 'landlord/will_arrive_soon.html', context)


def upcoming(request):
    """Предстоящие."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    upcoming = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.start_date > date.today() + timedelta(1)):
                upcoming.append(reserv)
    context = {'upcoming': upcoming}
    return render(request, 'landlord/upcoming.html', context)


def personal_data(request):
    context = CustomUser.objects.get(id=request.user.id)
    return render(request, 'accounts/personal_data.html', {'user': context})
