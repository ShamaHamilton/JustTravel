from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.core.paginator import Paginator

from .models import Localities, Places


def home(request):
    """Домашнаяя страница."""
    places = Places.objects.filter(is_published=True).select_related()
    localities = Localities.objects.filter(is_published=True)
    context = {
        'places': places,
        'localities': localities,
    }
    return render(request, 'blogs/home.html', context)


class LocalitiesView(ListView):
    """Список населенных пунктов."""
    model = Localities
    template_name = 'blogs/locality_list.html'
    context_object_name = 'localities_list'
    allow_empty = True
    paginate_by = 5

    def get_queryset(self):
        """Метод для фильтрации объектов по условию."""
        return Localities.objects.filter(is_published=True).prefetch_related('places')


class LicalityDetailView(DetailView):
    """Детальная информация о населенном пункте."""
    model = Localities
    template_name = 'blogs/locality_detail.html'
    context_object_name = 'locality'

    def get_context_data(self, **kwargs):
        """Метод для вывода динамичных данных."""
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        return context


def places_list_view(request):
    """Список интересных мест."""
    places_list = Places.objects.filter(is_published=True)
    paginator = Paginator(places_list, 5)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    context = {
        'page_obj': page_objects,
    }
    return render(request, 'blogs/places_list.html', context)


def place_detail_view(request, slug):
    """Детальная информация об интересном месте."""
    place = Places.objects.get(slug=slug)
    place.views += 1
    place.save()
    context = {
        'place': place,
    }
    return render(request, 'blogs/place_detail.html', context)