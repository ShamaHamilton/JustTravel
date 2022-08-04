from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    """Форма регистрации."""
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона'
        }),
    )
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя'
        }),
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Фамилия'
        }),
    )
    email = forms.EmailField(
        label='',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        }),
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        }),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль'
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'email')


class UserLoginForm(AuthenticationForm):
    """Форма аутентификации"""
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона',
            'id': 'id_phone'
        }),
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль'
        })
    )
