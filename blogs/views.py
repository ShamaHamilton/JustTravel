from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import F

import rooms

from .models import Localities, InterestingPlaces
from rooms.models import RoomsApplicationModel


def home(request):
    places_view = InterestingPlaces.objects.filter(is_published=True)
    localities_view = Localities.objects.filter(is_published=True)
    rooms_view = RoomsApplicationModel.objects.filter(status=True)
    context = {
        'places_view': places_view,
        'localities_view': localities_view,
        'rooms_view': rooms_view,
    }
    return render(request, 'blogs/home.html', context)


class LocalitiesView(ListView):
    model = Localities
    template_name = 'blogs/locality_list.html'
    context_object_name = 'localities_list'
    allow_empty = True

    def get_queryset(self):
        """Метод для фильтрации объектов по условию."""
        return Localities.objects.filter(is_published=True)


class LocalitiesDetailView(DetailView):
    model = Localities
    template_name = 'blogs/locality_detail.html'
    context_object_name = 'localities_item'

    def get_context_data(self, **kwargs):
        """Метод для вывода динамичных данных."""
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

class InterestingPlacesView(ListView):
    model = InterestingPlaces
    template_name = 'blogs/places_list.html'
    context_object_name = 'places_list'

    def get_context_data(self, **kwargs):
        """Метод для вывода динамичных данных."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        """Метод фильтрации объекта по условию."""
        return InterestingPlaces.objects.filter(is_published=True)


class InterestingPlacesDetailView(DetailView):
    model = InterestingPlaces
    template_name = 'blogs/places_detail.html'
    context_object_name = 'place'

    def get_context_data(self, **kwargs):
        """Метод для вывода динамичных данных."""
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context