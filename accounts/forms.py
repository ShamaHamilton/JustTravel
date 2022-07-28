from django.forms.models import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class UserRegisterForm(ModelForm):
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
        label='Пароль',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        }),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль'
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    """Форма аутентификации"""
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона'
        }),
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль'
        })
    )
