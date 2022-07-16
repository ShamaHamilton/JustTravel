from django.forms.models import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation, RoomsApplicationModel


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
        exclude = ('name_reserv', 'apartment', 'days_total', 'price_total', 'status')

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date < start_date:
            raise ValidationError('Некорректная дата выезда')
        return end_date
