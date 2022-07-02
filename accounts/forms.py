from django.forms.models import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class UserRegisterForm(ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

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
        label='Номер телефона',
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
