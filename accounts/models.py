from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    """Менеджер для создания кастомных пользователей."""
    
    def create_user(self, phone, first_name, last_name, password=None, **kwargs):
        if not phone:
            raise ValueError('Пользователь должен иметь номер телефона')
        user = self.model(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name, password=None, **kwargs):
        """
        Создает и сохраняет суперпользователя с указанным номером телефона,
        именем, фамилией и паролем.
        """
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        user = self.create_user(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )
        user.save(using =self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель для регистрации нового пользователя."""
    phone = models.CharField(
        verbose_name='номер телефона',
        max_length=18,
        unique=True,
    )
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
    rents_apartment = models.BooleanField(default=False, verbose_name='арендодатель?')
    about = models.TextField(max_length=500, blank=True, verbose_name='о пользователе')
    last_login = models.DateTimeField(auto_now=True, verbose_name='последний вход')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='активный')
    is_staff = models.BooleanField(default=False, verbose_name='вход в админку')
    is_superuser = models.BooleanField(default=False, verbose_name='администратор')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'