from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Vacancy, Company

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy_list.html'
    context_object_name = 'vacancies'
    queryset = Vacancy.objects.filter(is_active=True)

class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancy_detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().position_name.name
        return context


class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ['position_name', 'salary_start', 'salary_end', 'currency', 'company', 'location', 'employment_type', 'technology', 'is_active']
    template_name = 'form.html'
    success_url = reverse_lazy('home')
    
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Vacancy'
        context['form_title'] = 'Create Vacancy'
        context['form_btn'] = 'Post'
        context['with_media'] = True
        return context

class VacancyUpdateView(UpdateView, LoginRequiredMixin):
    model = Vacancy
    fields = ['position_name', 'salary_start', 'salary_end', 'currency', 'company', 'location', 'employment_type', 'technology', 'is_active']
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    success_message = 'The vacancy post was successfully updated.'

    # def test_func(self):
    #     # Check if the authenticated user is the author of the blog
    #     return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Vacancy'
        context['form_title'] = 'Update Vacancy'
        context['form_btn'] = 'Update'
        # context['with_media'] = True
        return context

class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'vacancy_delete.html'
    success_url = reverse_lazy('home')

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
                Q(position_name__name__icontains=search_query) |  
                Q(salary_start__icontains=search_query) |  
                Q(company__name__icontains=search_query) |  
                Q(location__city__name__icontains=search_query) |  
                Q(employment_type__name__icontains=search_query) |  
                Q(technology__technology_name__icontains=search_query) 
            )

        return queryset.order_by('-salary_start') 

# @login_required
# def hide_vacancy(request, pk):
#     vacancy = get_object_or_404(Vacancy, pk=pk)
#     HiddenVacancies.objects.create(user=request.user, vacancy=vacancy)
#     return redirect('vacancy_list')

# @login_required
# def hidden_vacancies(request):
#     hidden_vacancies = HiddenVacancies.objects.filter(user=request.user)
#     return render(request, 'vacancies/hidden_vacancies.html', {'hidden_vacancies': hidden_vacancies})