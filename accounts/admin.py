from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """Форма для создания нового пользователя."""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('phone', 'password', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        """Сохраняет введенный пароль в хешированном виде."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Форма для редактирования пользовательских параметров."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'phone',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'email',
        )


class CreateUserAdmin(BaseUserAdmin):
    """Форма для добавления и изменения пользовательских экземпляров."""
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id',
        'phone',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'is_superuser',
    )
    list_display_links = ('id', 'phone', 'first_name', 'last_name',)
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': (
            'phone',
            'email',
            'password',
            'first_name',
            'last_name',
        )}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Прочее', {'fields': ('about', 'date_joined', 'last_login')}),
    )
    readonly_fields = ('date_joined', 'last_login',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'email', 'password'),
        }),
    )
    search_fields = ('phone', 'first_name', 'last_name',)
    ordering = ('-date_joined',)
    filter_horizontal = ()


admin.site.register(CustomUser, CreateUserAdmin)
admin.site.unregister(Group)

admin.site.site_title = 'JustTravel'
admin.site.site_header = 'JustTravel'