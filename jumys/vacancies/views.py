from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Vacancy


from django.db.models import Q
from django.views.generic import ListView
from .models import Vacancy

class HomePageView(ListView):
    model = Vacancy
    template_name = 'index.html'
    context_object_name = 'vacancies'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        queryset = Vacancy.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(position_name__title__icontains=search_query) |  # Adjust to correct field name
                Q(salary_start__icontains=search_query) |  # Adjust based on your model fields
                Q(company__name__icontains=search_query) |  # Adjust based on your model fields
                Q(location__name__icontains=search_query) |  # Adjust based on your model fields
                Q(employment_type__name__icontains=search_query) |  # Adjust based on your model fields
                Q(technology__name__icontains=search_query)  # Adjust based on your model fields
            )

        # Order by a specific field (for example, by position name)
        return queryset.order_by('-salary_start')  # Replace with your desired field for ordering
