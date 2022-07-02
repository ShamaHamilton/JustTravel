from django.views.generic import FormView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms import modelform_factory
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .models import CustomCreateUser
from .forms import CreateUserForm, UserLoginForm
from . import constants


def get_create_user_from_hash(session_hash):
    """Находит и возвращает еще не завершенную сессию CustomCreateUser."""
    # ! TODO: реализовать ограничение по времени на хранение хеша
    return CustomCreateUser.objects.filter(
        session_hash=session_hash,
    ).exclude(
        stage=constants.COMPLETE
    ).first()


class CreateUserView(FormView):
    template_name = 'accounts/register.html'
    context_object_name = 'user'                         # ! ! ! ! ! ! ! !
    create_user = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        """
        Ищет существующий экземпляр CustomCreateUser чье поле session_hash
        соответствует текущему сеансу пользователя.
        """
        session_hash=request.session.get('session_hash', None)
        self.create_user = get_create_user_from_hash(session_hash)
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Проверяет чтобы все поля получили допустимые значения."""
        self.request.session['session_hash'] = form.instance.session_hash
        current_stage = form.cleaned_data.get('stage')
        # Переход к следующему этапу.
        new_stage = constants.STAGE_ORDER[
            constants.STAGE_ORDER.index(current_stage)+1
        ]
        form.instance.stage = new_stage
        form.save()
        if new_stage == constants.COMPLETE:
            # ! прописать адрес для перенаправления после завершения регистрации
            return redirect(reverse('blogs:home'))
        return redirect(reverse('accounts:register'))   # ! ! ! ! ! ! ! !

    def get_form_class(self):
        """Возвращает класс формы с полями текущей стадии выполнения приложения."""
        # Если нашелся CreateUser, который соответствует текущему хешу сеанса,
        # обратиться к его атрибуту stage, чтобы решить на какой стадии регистрации
        # находится пользователь. В противном случае предполагается, что пользователь
        # находится на стации 1.
        stage = self.create_user.stage if self.create_user else constants.STAGE_1
        # Получить поля формы, соответствующие текущему этапу
        fields = CustomCreateUser.get_fields_by_stage(stage)
        # Использовать эти поля для динамического создания формы 
        # с помощью "modelform_factory"
        return modelform_factory(CustomCreateUser, CreateUserForm, fields)

    def get_form_kwargs(self):
        """Проверяем что Django использует тот же экземпляр CustomCreateUser,
        с которым работаем.
        """
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.create_user
        return kwargs


def user_login(request):
    """Функция авторизации пользователей."""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blogs:home')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    """Функция выхода пользователя из системы."""
    logout(request)
    return redirect('accounts:login')
