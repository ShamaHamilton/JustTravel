from . import constants
from .forms import CreateRoomForm, ReservationForm
from .models import RoomsApplicationModel
from django.views.generic import FormView, ListView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms import modelform_factory
# from django.contrib import messages

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
        # Если нашелся RentApplication, который соответствует текущему хешу сеанса,
        # обратиться к его атрибуту stage, чтобы решить на какой стадии регистрации
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

    def get_queryset(self):
        """Метод для фильтрации объектов по условию."""
        return RoomsApplicationModel.objects.filter(status=True)


def room_reservation(request, pk):
    room_details = RoomsApplicationModel.objects.get(pk=pk)
    if request.method == 'POST':
        room_reserv = ReservationForm(request.POST)
        if room_reserv.is_valid():
            room_reserv.instance.name_reserv = request.user
            room_reserv.instance.apartment = room_details
            delta = room_reserv.instance.end_date - room_reserv.instance.start_date
            room_reserv.instance.days_total = delta.days
            room_reserv.instance.price_total = delta.days * room_details.price
            room_reserv.save()
            return redirect('blogs:home')
    else:
        room_reserv = ReservationForm()
    context = {
        'room_details': room_details,
        'room_reserv': room_reserv,
    }
    return render(request, template_name='rooms/room_detail.html', context=context)
