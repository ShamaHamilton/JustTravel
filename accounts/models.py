import hashlib, random, sys
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from . import constants


class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, phone, first_name, last_name, password=None, **kwargs):
        """
        Создает и сохраняет суперпользователя и указанным номером телефона,
        именем, фамилией и паролем.
        """
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        user = self.model(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


def create_session_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
    return hash.hexdigest()


class CustomCreateUser(AbstractBaseUser, PermissionsMixin):
    """Модель для регистрации нового пользователя."""
    # session_hash нужен для получения правильного экземпляра модели,
    # связать отдельные GET и POST запросы
    session_hash = models.CharField(max_length=40, unique=True)
    # stage позволяет определить какие поля выводить на каждом этапе
    stage = models.CharField(max_length=10, default=constants.STAGE_1)
    # шаг 1
    phone = models.CharField(
        verbose_name='номер телефона',
        max_length=12,
        unique=True,
    )
    # шаг 2
    password = models.CharField(
        verbose_name='пароль',
        max_length=128,
        blank=True,
    )
    # шаг 3
    first_name = models.CharField(
        verbose_name='имя',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=50,
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        blank=True,
    )
    # дополнительная информация
    about = models.TextField(max_length=500, blank=True, verbose_name='о пользователе')
    last_login = models.DateTimeField(auto_now=True, verbose_name='последний вход')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='активный')
    is_staff = models.BooleanField(default=False, verbose_name='вход в админку')
    is_superuser = models.BooleanField(default=False, verbose_name='администратор')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    # Скрытые поля для динамической формы
    hidden_fields = ['stage']
    # Обязательные поля для динамической формы
    required_fields = ['phone', 'password', 'first_name', 'last_name']

    @staticmethod
    def get_fields_by_stage(stage):
        """Разбивает поля модели на группы по стадиям."""
        fields = ['stage']
        if stage == constants.STAGE_1:
            fields.extend(['phone'])
        elif stage == constants.STAGE_2:
            fields.extend(['password'])
        elif stage == constants.STAGE_3:
            fields.extend(['first_name', 'last_name', 'email'])
        return fields

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.session_hash:
            while True:
                session_hash = create_session_hash()
                if CustomCreateUser.objects.filter(session_hash=session_hash).count() == 0:
                    self.session_hash = session_hash
                    break

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'