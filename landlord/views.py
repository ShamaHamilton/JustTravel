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
    reservs = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.end_date == date.today() or
                reserv.end_date == date.today() + timedelta(1) and
                reserv.start_date < date.today()):
                reservs.append(reserv)
    if reservs:
        context = {'reservs': reservs}
    else:
        message = 'Нет гостей, выезжающих сегодня.'
        context = {'message': message}
    return render(request, 'landlord/account.html', context)


def reside(request):
    """Проживают."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    reservs = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.start_date < date.today() and
                reserv.end_date > date.today() + timedelta(1)):
                reservs.append(reserv)
    if reservs:
        context = {'reservs': reservs}
    else:
        message = 'Сейчас у вас нет гостей.'
        context = {'message': message}
    return render(request, 'landlord/account.html', context)


def will_arrive_soon(request):
    """Скоро приедут."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    reservs = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.start_date == date.today() or
                reserv.start_date == date.today() + timedelta(1)):
                reservs.append(reserv)
    if reservs:
        context = {'reservs': reservs}
    else:
        message = 'Нет гостей, прибывающих сегодня или завтра.'
        context = {'message': message}
    return render(request, 'landlord/account.html', context)


def upcoming(request):
    """Предстоящие."""
    landlord_apartments = RoomsApplicationModel.objects.filter(
        landlord_id=request.user
    )
    reservs = []
    for apartment in landlord_apartments:
        apartment_reservs = Reservation.objects.filter(
            apartment_id=apartment.pk
        )
        for reserv in apartment_reservs:
            if (reserv.start_date > date.today() + timedelta(1)):
                reservs.append(reserv)
    if reservs:
        context = {'reservs': reservs}
    else:
        message = 'У вас нет предстоящих бронирований.'
        context = {'message': message}
    return render(request, 'landlord/account.html', context)


def personal_data(request):
    context = CustomUser.objects.get(id=request.user.id)
    return render(request, 'landlord/personal_data.html', {'user': context})
