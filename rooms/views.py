from .forms import CreateRoomForm, ReservationForm, RatingForm, ReviewForm
from .models import Rating, RoomsApplicationModel, Reservation
from .import constants

from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms import modelform_factory
from django.contrib import messages
from datetime import date, timedelta
from django.contrib.auth import get_user_model
User = get_user_model()


def get_create_room_from_hash(session_hash):
    """Находит и возвращает еще не завершенную сессию CustomCreateUser."""
    # ! TODO: реализовать ограничение по времени на хранение хеша
    return RoomsApplicationModel.objects.filter(
        session_hash=session_hash,
    ).exclude(
        stage=constants.COMPLETE
    ).first()


class CreateRoomView(FormView):
    template_name = 'rooms/room_create.html'
    create_room = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        """
        Ищет существующий экземпляр RoomsApplicationModel чье поле session_hash
        соответствует текущему сеансу пользователя.
        """
        session_hash = request.session.get('session_hash', None)
        self.create_room = get_create_room_from_hash(session_hash)
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Проверяет чтобы все поля получили допустимые значения."""
        self.request.session['session_hash'] = form.instance.session_hash
        form.instance.landlord = self.request.user
        current_stage = form.cleaned_data.get('stage')
        # Переход к следующему этапу.
        new_stage = constants.STAGE_ORDER[
            constants.STAGE_ORDER.index(current_stage)+1
        ]
        form.instance.stage = new_stage
        form.save()
        if new_stage == constants.COMPLETE:
            # ! прописать адрес для перенаправления после добавления жилья
            return redirect(reverse('blogs:home'))
        return redirect(reverse('rooms:create_room'))

    def get_form_class(self):
        """Возвращает класс формы с полями текущей стадии выполнения приложения."""
        # Если нашелся RoomsApplicationModel, который соответствует текущему хешу сеанса,
        # обратиться к его атрибуту stage, чтобы решить на какой стадии создания
        # находится пользователь. В противном случае предполагается, что пользователь
        # находится на стации 1.
        stage = self.create_room.stage if self.create_room else constants.STAGE_1
        # Получить поля формы, соответствующие текущему этапу
        fields = RoomsApplicationModel.get_fields_by_stage(stage)
        # Использовать эти поля для динамического создания формы
        # с помощью "modelform_factory"
        return modelform_factory(RoomsApplicationModel, CreateRoomForm, fields)

    def get_form_kwargs(self):
        """Проверяем что Django использует тот же экземпляр RentApplicationModel,
        с которым работаем.
        """
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.create_room
        return kwargs


class RoomsView(ListView):
    model = RoomsApplicationModel
    template_name = 'rooms/rooms_list.html'
    context_object_name = 'rooms_list'
    paginate_by = 1

    def get_queryset(self):
        """Метод для фильтрации объектов по условию."""
        return RoomsApplicationModel.objects.filter(status=True)


def room_detail_view(request, pk):
    """Функция для просмотра жилья."""
    room = RoomsApplicationModel.objects.get(pk=pk)
    # Извлечение броней связанных с данных жильем
    reservs = Reservation.objects.filter(apartment_id=room.pk)
    reserv_days_in = []      # Список дат для блокировки
    reserv_days_out = []     # Список дат для брокировки
    # Извлечение списка зарезервированных дат для передачи в календарь
    for reserv in reservs:
        if reserv.end_date >= date.today() and reserv.status:
            start_day = reserv.start_date
            end_day = reserv.end_date
            delta_days = int((end_day - start_day).days)
            day = 0
            for day in range(delta_days):
                reserv_days_in.append(start_day.strftime("%d-%m-%Y"))
                reserv_days_out.append(end_day.strftime("%d-%m-%Y"))
                start_day += timedelta(days=1)
                end_day -= timedelta(days=1)
    reserv_days_in.sort()   # Сортировка дат по возрастанию
    reserv_days_out.sort()  # Сортировка дат по возрастанию
    room.views += 1
    room.save()
    if request.method == 'POST':
        if 'reserv' in request.POST:
            room_reserv = ReservationForm(request.POST)
            if room_reserv.is_valid():
                room_reserv.instance.name_reserv = request.user
                room_reserv.instance.apartment = room
                delta = room_reserv.instance.end_date - room.instance.start_date
                room_reserv.instance.days_total = delta.days
                room_reserv.instance.price_total = delta.days * room.price
                room_reserv.save()
                return redirect('accounts:account')
        elif 'review' in request.POST:
            review = ReviewForm(request.POST)
            if review.is_valid():
                review.instance.user_feedback = request.user
                review.instance.apartment = room
                review.save()
                return redirect('accounts:account')
    room_reserv = ReservationForm()
    review = ReviewForm()
    context = {
        'room': room,
        'reserv': room_reserv,
        'reservs': reservs,
        'reserv_days_in': reserv_days_in,
        'reserv_days_out': reserv_days_out,
        'review': review,
    }
    context['star_form'] = RatingForm()
    context['review_form'] = ReviewForm()
    return render(request, template_name='rooms/room_detail.html', context=context)


# class RoomDetailView(DetailView):
#     model = RoomsApplicationModel
#     template_name = 'rooms/room_detail.html'
#     context_object_name = 'room'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reserv'] = ReservationForm()
#         context['star_form'] = RatingForm()
#         return context


class AddStarRating(View):
    """Добавление рейтинга жилья."""
    def post(self, request):
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


class AddReview(View):
    """Отзывы."""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        apartment = RoomsApplicationModel.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.apartment = apartment
            form.save()
        return redirect(apartment.get_absolute_url())


def room_reser_details(request, pk):
    current_reserv = Reservation.objects.get(pk=pk)
    if request.method == 'POST':
        current_reserv.status = False
        current_reserv.save()
        messages.success(request, 'Бронь отменена')
        return redirect('accounts:account')
    context = {
        'current_reserv': current_reserv,
    }
    return render(request, 'rooms/room_reserv_details.html', context)
