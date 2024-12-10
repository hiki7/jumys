# vacancies/views.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from users.permissions import IsSeeker, IsAdminOrHR, IsAdminOrCompanyManager
from .models import Vacancy
from seekers.models import Application
from .forms import VacancyForm
from django.views import View

# Vacancy Views
class VacancyListView(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        return Vacancy.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role in ['admin', 'hr']:
            context['can_create_vacancy'] = True
        else:
            context['can_create_vacancy'] = False
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        vacancy = self.get_object()
        context['can_edit'] = (
            user.is_authenticated and (
                user.role == 'admin' or
                user.role == 'hr' or
                user in vacancy.company.managers.all() or
                user == vacancy.company.head_manager
            )
        )
        return context


class VacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    success_url = reverse_lazy("vacancy_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.role == 'hr':
            company = form.cleaned_data.get('company')
            if not self.request.user.companies_managed.filter(id=company.id).exists():
                form.add_error('company', "You do not have permission to create a vacancy for this company.")
                return self.form_invalid(form)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ['admin', 'hr']:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to create a vacancy.")
            return redirect("vacancy_list")


class VacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    success_url = reverse_lazy("vacancy_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.role == 'hr':
            company = form.cleaned_data.get('company')
            if not self.request.user.companies_managed.filter(id=company.id).exists():
                form.add_error('company', "You do not have permission to edit a vacancy for this company.")
                return self.form_invalid(form)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        vacancy = self.get_object()
        if request.user.role == 'admin' or \
           (request.user.role == 'hr' and request.user.companies_managed.filter(id=vacancy.company.id).exists()):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to edit this vacancy.")
            return redirect("vacancy_list")


class VacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacancy
    template_name = "vacancies/vacancy_confirm_delete.html"
    success_url = reverse_lazy("vacancy_list")

    def dispatch(self, request, *args, **kwargs):
        vacancy = self.get_object()
        if request.user.role == 'admin' or \
           (request.user.role == 'hr' and request.user.companies_managed.filter(id=vacancy.company.id).exists()):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to delete this vacancy.")
            return redirect("vacancy_list")


# Application Views
class ApplyToVacancyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=kwargs['pk'])
        user_profile = getattr(request.user, 'profile', None)

        if not vacancy.is_active:
            messages.error(request, "This vacancy is not active.")
            return redirect("vacancy_detail", pk=vacancy.pk)

        if not user_profile:
            messages.error(request, "You must complete your profile to apply for a vacancy.")
            return redirect("profile")

        if Application.objects.filter(user_profile=user_profile, vacancy=vacancy).exists():
            messages.error(request, "You have already applied to this vacancy.")
            return redirect("vacancy_detail", pk=vacancy.pk)

        # Create the application
        Application.objects.create(user_profile=user_profile, vacancy=vacancy)
        messages.success(request, "You have successfully applied to the vacancy.")
        return redirect("vacancy_detail", pk=vacancy.pk)

class BookmarkVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = "vacancies/bookmark_vacancy.html"

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()
        user = request.user

        if not vacancy.is_active:
            messages.error(request, "Vacancy does not exist or is inactive.")
            return redirect("vacancy_list")

        if vacancy.bookmarked_by.filter(id=user.id).exists():
            messages.error(request, "Vacancy is already bookmarked.")
            return redirect("vacancy_list")

        vacancy.bookmarked_by.add(user)
        messages.success(request, "Vacancy bookmarked successfully.")
        return redirect("vacancy_list")

    def delete(self, request, *args, **kwargs):
        vacancy = self.get_object()
        user = request.user

        if not vacancy.bookmarked_by.filter(id=user.id).exists():
            messages.error(request, "Vacancy is not bookmarked.")
            return redirect("vacancy_list")

        vacancy.bookmarked_by.remove(user)
        messages.success(request, "Vacancy removed from bookmarks.")
        return redirect("vacancy_list")
