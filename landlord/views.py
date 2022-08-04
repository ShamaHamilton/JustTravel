from django.shortcuts import render
from django.db.models import Q

from datetime import date, timedelta

from accounts.models import CustomUser
from rooms.models import Reservation


def account(request):
    """Аккаунт арендодателя."""
    return render(request, 'landlord/account.html')


def leaving(request):
    """Выезжают."""
    reservs = Reservation.objects.filter(
        Q(apartment__landlord=request.user),
        Q(apartment__status=True),
        Q(start_date__lt=date.today()),
        Q(end_date=date.today()) |
        Q(end_date=date.today()+timedelta(1))
    ).select_related()
    if reservs:
        context = {'reservs': reservs}
    else:
        context = {'message': 'Нет гостей, выезжающих сегодня или завтра.'}
    return render(request, 'landlord/account.html', context)


def reside(request):
    """Проживают."""
    reservs = Reservation.objects.filter(
        Q(apartment__landlord=request.user),
        Q(apartment__status=True),
        Q(start_date__lt=date.today()),
        Q(end_date__gt=date.today())
    ).select_related()
    if reservs:
        context = {'reservs': reservs}
    else:
        context = {'message': 'Сейчас у вас нет гостей.'}
    return render(request, 'landlord/account.html', context)


def will_arrive_soon(request):
    """Скоро приедут."""
    reservs = Reservation.objects.filter(
        Q(apartment__landlord=request.user),
        Q(apartment__status=True),
        Q(start_date=date.today()) |
        Q(start_date=date.today()+timedelta(1))
    ).select_related()
    if reservs:
        context = {'reservs': reservs}
    else:
        context = {'message': 'Нет гостей, прибывающих сегодня или завтра.'}
    return render(request, 'landlord/account.html', context)


def upcoming(request):
    """Предстоящие."""
    reservs = Reservation.objects.filter(
        Q(apartment__landlord=request.user),
        Q(apartment__status=True),
        Q(status=True),
        Q(start_date__gte=date.today())
    ).select_related()
    if reservs:
        context = {'reservs': reservs}
    else:
        context = {'message': 'У вас нет предстоящих бронирований.'}
    return render(request, 'landlord/account.html', context)


def personal_data(request):
    """Личные данные арендодателя."""
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'landlord/personal_data.html', {'user': user})
