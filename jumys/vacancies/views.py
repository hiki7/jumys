from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Vacancy, HiddenVacancies, Company

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy_list.html'
    context_object_name = 'vacancies'
    queryset = Vacancy.objects.filter(is_active=True)

class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancies/vacancy_detail.html'
    context_object_name = 'vacancy'

class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ['position_name', 'salary_start', 'salary_end', 'currency', 'company', 'location', 'employment_type', 'technology', 'is_active']
    template_name = 'vacancies/vacancy_form.html'
    success_url = reverse_lazy('vacancy_list')

class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ['position_name', 'salary_start', 'salary_end', 'currency', 'company', 'location', 'employment_type', 'technology', 'is_active']
    template_name = 'vacancies/vacancy_form.html'
    success_url = reverse_lazy('vacancy_list')

class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'vacancies/vacancy_confirm_delete.html'
    success_url = reverse_lazy('vacancy_list')

@login_required
def hide_vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    HiddenVacancies.objects.create(user=request.user, vacancy=vacancy)
    return redirect('vacancy_list')

@login_required
def hidden_vacancies(request):
    hidden_vacancies = HiddenVacancies.objects.filter(user=request.user)
    return render(request, 'vacancies/hidden_vacancies.html', {'hidden_vacancies': hidden_vacancies})

class CompanyListView(ListView):
    model = Company
    template_name = 'vacancies/company_list.html'
    context_object_name = 'companies'

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
