from multiprocessing import context
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages

from datetime import date

from .forms import UserRegisterForm, UserLoginForm
from rooms.models import Reservation


def user_account(request):
    """Личный кабинет пользователя."""
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
    return render(request, 'accounts/account.html', context)


def user_active_reservs(request):
    user_reservs = Reservation.objects.filter(name_reserv_id=request.user)
    active_reservs = []
    for user_reserv in user_reservs:
        if user_reserv.end_date >= date.today() and user_reserv.status:
            active_reservs.append(user_reserv)
    context = {
        'active_reservs': active_reservs,
    }
    return render(request, 'accounts/active.html', context)

def user_inactive_reservs(request):
    user_reservs = Reservation.objects.filter(name_reserv_id=request.user)
    inactive_reservs = []
    for user_reserv in user_reservs:
        if user_reserv.end_date < date.today():
            inactive_reservs.append(user_reserv)
    context = {
        'inactive_reservs': inactive_reservs,
    }
    return render(request, 'accounts/inactive.html', context)


def user_canceled_reservs(request):
    user_reservs = Reservation.objects.filter(name_reserv_id=request.user)
    canceled_reservs = []
    for user_reserv in user_reservs:
        if user_reserv.status == False:
            canceled_reservs.append(user_reserv)
    context = {
        'canceled_reservs': canceled_reservs,
    }
    return render(request, 'accounts/canceled.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect(reverse('blogs:home'))
        else:
            messages.error(request, 'Ошибка регистрации(')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, template_name='accounts/register.html', context=context)


def user_login(request):
    """Функция авторизации пользователей."""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('blogs:home'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    """Функция выхода пользователя из системы."""
    logout(request)
    return redirect('accounts:login')
