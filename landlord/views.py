from django.shortcuts import render

from accounts.models import CustomUser
from landlord.functions.landlord_func import get_landlord_list


def account(request):
    context = get_landlord_list(request)
    return render(request, 'landlord/account.html', context)


def leaving(request):
    """Выезжают."""
    context = get_landlord_list(request)
    return render(request, 'landlord/leaving.html', context)


def reside(request):
    """Проживают."""
    context = get_landlord_list(request)
    return render(request, 'landlord/reside.html', context)


def will_arrive_soon(request):
    """Скоро приедут."""
    context = get_landlord_list(request)
    return render(request, 'landlord/will_arrive_soon.html', context)


def upcoming(request):
    """Предстоящие."""
    context = get_landlord_list(request)
    return render(request, 'landlord/upcoming.html', context)


def personal_data(request):
    context = CustomUser.objects.get(id=request.user.id)
    return render(request, 'accounts/personal_data.html', {'user': context})
