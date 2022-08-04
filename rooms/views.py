from .forms import CreateRoomForm, ReservationForm, RatingForm, ReviewForm
from .models import Rating, RoomsModel, Reservation, Reviews, RatingStar

from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.db.models import Avg
User = get_user_model()


class CreateRoomView(CreateView):
    """Добавление жилья."""
    form_class = CreateRoomForm
    template_name = 'rooms/room_create.html'


class RoomsView(ListView):
    """Список доступного жилья."""
    queryset = RoomsModel.objects.filter(status=True)
    template_name = 'rooms/rooms_list.html'
    context_object_name = 'rooms_list'
    paginate_by = 5


def get_reservs_date(kwargs):
    """Возвращает забронированные (занятые) даты для конкреного жилья."""
    # Извлечение броней связанных с данным жильем
    reservs = Reservation.objects.filter(
        Q(apartment_id=kwargs['pk']),
        Q(status=True),
        Q(end_date__gt=date.today())
    )
    reserv_days_in = []      # Список занятых дат прибытия
    reserv_days_out = []     # Список занятых дат выезда
    # Извлечение списка зарезервированных дат для передачи в календарь
    for reserv in reservs:
        start_day = reserv.start_date
        end_day = reserv.end_date
        delta_days = int((end_day - start_day).days)
        day = 0
        for day in range(delta_days):
            reserv_days_in.append(start_day.strftime("%d-%m-%Y"))
            reserv_days_out.append(end_day.strftime("%d-%m-%Y"))
            start_day += timedelta(days=1)
            end_day -= timedelta(days=1)
    reserv_days_out.append(date.today().strftime("%d-%m-%Y"))
    return(reserv_days_in, reserv_days_out)


class RoomDetailView(DetailView):
    """Подробная информация о жилье."""
    model = RoomsModel
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'
    queryset = RoomsModel.objects.select_related('landlord')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reserv_days_in, reserv_days_out = get_reservs_date(self.kwargs)
        rating = RatingStar.objects.filter(
            Q(rating__apartment=self.kwargs['pk']),
            Q(rating__status=True)
        ).aggregate(Avg('value'))
        reviews = Reviews.objects.filter(
            Q(apartment=self.kwargs['pk']),
            Q(status=True)
        ).select_related()
        context['rating'] = rating
        context['reviews'] = reviews
        context['reserv'] = ReservationForm()
        context['star_form'] = RatingForm()
        context['review_form'] = ReviewForm()
        context['reserv_days_in'] = reserv_days_in
        context['reserv_days_out'] = reserv_days_out
        self.object.views += 1
        self.object.save()
        return context


class AddReserv(View):
    """Резер жилья."""

    def post(self, request, pk):
        if request.user.is_authenticated:
            form = ReservationForm(request.POST)
            apartment = RoomsModel.objects.get(pk=pk)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.apartment_id = apartment.id
                start_date = form.start_date
                end_date = form.end_date
                delta = (end_date - start_date).days
                form.days_total = delta
                form.price_total = delta * apartment.price
                form.save()
            return redirect('accounts:account')
        else:
            return redirect('accounts:register')


class AddStarRating(View):
    """Добавление рейтинга жилья."""

    def post(self, request):
        if request.user.is_authenticated:
            form = RatingForm(request.POST)
            if form.is_valid():
                Rating.objects.update_or_create(
                    user=request.user,
                    apartment_id=int(request.POST.get('apartment')),
                    defaults={'star_id': int(request.POST.get('star'))}
                )
                return HttpResponse(status=201)
            else:
                return HttpResponse(status=400)
        else:
            return redirect('accounts:register')


class AddReview(View):
    """Отзывы."""

    def post(self, request, pk):
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            apartment = RoomsModel.objects.get(pk=pk)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.apartment = apartment
                form.save()
            return redirect(apartment.get_absolute_url())
        else:
            return redirect('accounts:register')


def room_reser_details(request, pk):
    """Детали забронированного жилья в ЛК."""
    current_reserv = Reservation.objects.get(pk=pk)
    if request.method == 'POST':
        current_reserv.status = False
        current_reserv.save()
        return redirect('accounts:account')
    context = {
        'current_reserv': current_reserv,
    }
    return render(request, 'rooms/room_reserv_details.html', context)


class Search(ListView):
    """Поиск жилья."""
    template_name = 'rooms/rooms_list.html'
    context_object_name = 'rooms_list'
    paginate_by = 1

    def get_queryset(self):
        queryset = RoomsModel.objects.filter(
            Q(status=True),
            Q(location__icontains=self.request.GET.get('place'))
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = f"place={self.request.GET.get('place')}&"
        return context
