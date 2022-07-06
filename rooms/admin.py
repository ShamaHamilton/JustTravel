from django.contrib import admin
from django import forms

from .models import RoomsApplicationModel, Reservation


class RoomCreationForm(forms.ModelForm):
    """Форма для создания жилья из админки."""

    class Meta:
        model = RoomsApplicationModel
        fields = (
            'landlord',
            'status',
            'housing_header',
            'housing_description',
            'housing',
            'housing_type',
            'offer_type',
            'location',
            'number_of_guests',
            'special_amenities',
            'popular_amenities',
            'safety',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            'price',
        )


class RoomChangeForm(forms.ModelForm):
    """Форма для редактирования пользовательских параметров."""

    class Meta:
        model = RoomsApplicationModel
        fields = (
            'landlord',
            'status',
            'housing_header',
            'housing_description',
            'housing',
            'housing_type',
            'offer_type',
            'location',
            'number_of_guests',
            'special_amenities',
            'popular_amenities',
            'safety',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            'price',
        )


class RoomAdmin(admin.ModelAdmin):
    """Форма для добавления и изменения пользовательских экземпляров."""
    form = RoomCreationForm
    add_form = RoomChangeForm
    list_display = (
        'id',
        'landlord',
        'status',
        'housing',
        'housing_type',
        'offer_type',
        'price',
    )
    list_display_links = ('id', 'landlord')
    search_fields = ('landlord',)
    list_editable = ('status',)
    list_filter = ('landlord', 'status')
    fields = (
        'landlord',
        'status',
        'housing_header',
        'housing_description',
        'housing',
        'housing_type',
        'offer_type',
        'location',
        'number_of_guests',
        'special_amenities',
        'popular_amenities',
        'safety',
        'photo1',
        'photo2',
        'photo3',
        'photo4',
        'photo5',
        'price',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True


admin.site.register(RoomsApplicationModel, RoomAdmin)


class ReservationForm(forms.ModelForm):
    """Форма для создания жилья из админки."""

    class Meta:
        model = RoomsApplicationModel
        fields = '__all__'
        exclude = ('created_at',)

class ReservationAdmin(admin.ModelAdmin):
    """Форма для добавления и изменения пользовательских экземпляров."""
    list_display = (
        'id',
        'name_reserv',
        'apartment',
        'start_date',
        'end_date',
        'days_total',
        'price_total',
    )
    list_display_links = ('id', 'name_reserv', 'apartment',)
    # search_fields = ('apartment',)
    # list_editable = ('',)
    # list_filter = ('apartment',)
    fields = (
        'apartment',
        'start_date',
        'end_date',
        'name_reserv',
        'days_total',
        'price_total',
        'status',
    )
    # save_on_top = True


admin.site.register(Reservation, ReservationAdmin)
