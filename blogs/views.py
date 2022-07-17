from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.core.paginator import Paginator

from .models import Localities, InterestingPlaces


def home(request):
    places_view = InterestingPlaces.objects.filter(is_published=True)
    localities_view = Localities.objects.filter(is_published=True)
    context = {
        'places_view': places_view,
        'localities_view': localities_view,
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
        return Localities.objects.filter(is_published=True)


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
        self.object.refresh_from_db()
        return context


def places_list_view(request):
    """Список интересных мест."""
    places_list = InterestingPlaces.objects.filter(is_published=True)
    paginator = Paginator(places_list, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    context = {
        'page_obj': page_objects,
    }
    return render(request, 'blogs/places_list.html', context)


def place_detail_view(request, slug):
    """Детальная информация об интересном месте."""
    place = InterestingPlaces.objects.get(slug=slug)
    place.views += 1
    place.save()
    context = {
        'place': place,
    }
    return render(request, 'blogs/place_detail.html', context)