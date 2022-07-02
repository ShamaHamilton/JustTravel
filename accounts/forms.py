from django.forms.models import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class CreateUserForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = self.instance.required_fields
        hidden_fields = self.instance.hidden_fields
        for field in self.fields:
            if field in required_fields:
                self.fields.get(field).required = True
            if field in hidden_fields:
                self.fields.get(field).widget = forms.HiddenInput()
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(str(password)) < 6:
            raise ValidationError('Введите корректный код')
        return password


class UserLoginForm(AuthenticationForm):
    """Форма аутентификации"""
    username = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
