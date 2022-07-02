from django.forms.models import ModelForm
from django import forms

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
        label='прибытие',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'},
        ),
    )
    end_date = forms.DateField(
        label='выезд',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ('name_reserv', 'apartment', 'days_total', 'price_total',)
        # fields = ('start_date', 'end_date',)

    # def clean_start_date(self):
    #     start_date = self.cleaned_data['start_date']
    #     if str(start_date) <= str(datetime.datetime.now()):
    #         ValidationError('некорректная дата прибытия')
    #     return start_date

    # def clean_end_date(self):
    #     start_date = self.cleaned_data['start_date']
    #     end_date = self.cleaned_data['end_date']
    #     if str(end_date) < str(start_date):
    #         ValidationError('Некорректная дата')
    #     return end_date

    # def clean_end_date(self):
    #     start_date = self.cleaned_data['start_date']
    #     start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
    #     end_date = self.cleaned_data['end_date']
    #     end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').days
    #     # days_total = self.cleaned_data['days_total']
    #     # price_total = self.cleaned_data['price_total']
    #     if start_date < end_date:
    #         self.days_total = end_date - start_date
    #         self.price_total = 1000
    #     return self.days_total, self.price_total