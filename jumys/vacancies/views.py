from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Vacancy, Company

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

# @login_required
# def hide_vacancy(request, pk):
#     vacancy = get_object_or_404(Vacancy, pk=pk)
#     HiddenVacancies.objects.create(user=request.user, vacancy=vacancy)
#     return redirect('vacancy_list')

# @login_required
# def hidden_vacancies(request):
#     hidden_vacancies = HiddenVacancies.objects.filter(user=request.user)
#     return render(request, 'vacancies/hidden_vacancies.html', {'hidden_vacancies': hidden_vacancies})

class CompanyListView(ListView):
    model = Company
    template_name = 'vacancies/company_list.html'
    context_object_name = 'companies'


class HomePageView(ListView):
    model = Vacancy
    template_name = 'index.html'
    context_object_name = 'vacancies'
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        queryset = Vacancy.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(position_name__title__icontains=search_query) |  
                Q(salary_start__icontains=search_query) |  
                Q(company__name__icontains=search_query) |  
                Q(location__name__icontains=search_query) |  
                Q(employment_type__name__icontains=search_query) |  
                Q(technology__name__icontains=search_query)  
            )

        return queryset.order_by('-salary_start')  
