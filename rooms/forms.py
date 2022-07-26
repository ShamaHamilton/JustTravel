from django.forms.models import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from datetime import date

from .models import (
    RoomsApplicationModel, Reservation,
    RatingStar, Rating, Reviews
)


class CreateRoomForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = self.instance.required_fields
        hidden_fields = self.instance.hidden_fields
        for field in self.fields:
            if field in required_fields:
                self.fields.get(field).required = True
            if field in hidden_fields:
                self.fields.get(field).widget = forms.HiddenInput()

    class Meta:
        model = RoomsApplicationModel
        exclude = ['landlord']


class ReservationForm(forms.ModelForm):
    """Форма для резервирования жилья."""
    start_date = forms.DateField(
        label='Прибытие',
        help_text='дата прибытия',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'type': 'date_in',
                'placeholder': 'Укажите дату',
            },
        ),
    )
    end_date = forms.DateField(
        label='Выезд',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'type': 'date_out',
                'placeholder': 'Укажите дату',
            },
        ),
    )
    guests = forms.IntegerField(
        label='Гостей',
        help_text='количество гостей',
        widget=forms.NumberInput(
            attrs={'placeholder': 'Гостей'}
        )
    )

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = (
            'user',
            'apartment',
            'days_total',
            'price_total',
            'status',
        )

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date < start_date or end_date <= date.today():
            raise ValidationError('Некорректная дата выезда')
        return end_date


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга."""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None,
    )

    class Meta:
        model = Rating
        fields = ('star',)


class ReviewForm(forms.ModelForm):
    """Форма отзывов."""
    review = forms.CharField(
        widget = forms.Textarea(
            attrs={
                'placeholder': 'Ваш отзыв',
                'rows': 5,
            },
        ),
    )

    class Meta:
        model = Reviews
        fields = ('review',)
