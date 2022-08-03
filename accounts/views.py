from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from datetime import date
from django.db.models import Q

from .models import CustomUser
from rooms.models import Reservation
from .forms import UserRegisterForm, UserLoginForm


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


def user_account(request):
    """Личный кабинет пользователя."""
    if request.user.rents_apartment:
        return redirect(reverse('landlord:account'))
    return render(request, 'accounts/account.html')


def active_reservs(request):
    active_reservs = Reservation.objects.filter(
        Q(user_id=request.user),
        Q(status=True),
        Q(end_date__gte=date.today())
    ).select_related()
    context = {
        'active_reservs': active_reservs
    }
    return render(request, 'accounts/account.html', context)


def inactive_reservs(request):
    inactive_reservs = Reservation.objects.filter(
        Q(user_id=request.user),
        Q(status=True),
        Q(end_date__lt=date.today())
    ).select_related()
    context = {
        'inactive_reservs': inactive_reservs
    }
    return render(request, 'accounts/account.html', context)


def canceled_reservs(request):
    canceled_reservs = Reservation.objects.filter(
        Q(user_id=request.user),
        Q(status=False)
    ).select_related()
    context = {
        'canceled_reservs': canceled_reservs
    }
    return render(request, 'accounts/account.html', context)


def personal_data(request):
    context = CustomUser.objects.get(id=request.user.id)
    return render(request, 'accounts/personal_data.html', {'user': context})
