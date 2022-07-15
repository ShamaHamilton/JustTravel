from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages

from .forms import UserRegisterForm, UserLoginForm
from accounts.functions.account_func import get_reservs_list, get_landlord_list


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
        context = get_landlord_list(request)
        return render(request, 'accounts/account_landlord.html', context)
    else:
        context = get_reservs_list(request)
        return render(request, 'accounts/account.html', context)


def user_active_reservs(request):
    context = get_reservs_list(request)
    return render(request, 'accounts/active.html', context)


def user_inactive_reservs(request):
    context = get_reservs_list(request)
    return render(request, 'accounts/inactive.html', context)


def user_canceled_reservs(request):
    context = get_reservs_list(request)
    return render(request, 'accounts/canceled.html', context)


def landlord_leaving(request):
    """Выезжают."""
    context = get_landlord_list(request)
    return render(request, 'accounts/leaving.html', context)


def landlord_reside(request):
    """Проживают."""
    context = get_landlord_list(request)
    return render(request, 'accounts/reside.html', context)


def landlord_will_arrive_soon(request):
    """Скоро приедут."""
    context = get_landlord_list(request)
    return render(request, 'accounts/will_arrive_soon.html', context)


def landlord_upcoming(request):
    """Предстоящие."""
    context = get_landlord_list(request)
    return render(request, 'accounts/upcoming.html', context)