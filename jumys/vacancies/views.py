# vacancies/views.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from users.permissions import IsSeeker, IsAdminOrHR, IsAdminOrCompanyManager
from .models import Vacancy
from seekers.models import Application, UserProfile
from .forms import VacancyForm


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
class ApplyToVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = "vacancies/apply_vacancy.html"

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist.")
            return redirect("vacancy_list")

        if not vacancy.is_active:
            messages.error(request, "Vacancy does not exist or is inactive.")
            return redirect("vacancy_list")

        if Application.objects.filter(user_profile=user_profile, vacancy=vacancy).exists():
            messages.error(request, "You have already applied to this vacancy.")
            return redirect("vacancy_list")

        Application.objects.create(user_profile=user_profile, vacancy=vacancy)
        messages.success(request, "You have successfully applied to the vacancy.")
        return redirect("vacancy_list")



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

class ManagerApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "vacancies/manager_applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        """
        Filter applications for the vacancies of companies where the user is a manager or head manager.
        """
        user = self.request.user
        return Application.objects.filter(
            vacancy__company__in=user.companies_managed.all() | user.companies_headed.all()
        ).select_related('user_profile__user', 'vacancy', 'vacancy__company')

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template, like the list of managed companies.
        """
        context = super().get_context_data(**kwargs)
        context['companies'] = self.request.user.companies_managed.all() | self.request.user.companies_headed.all()
        return context
    
class ToggleReviewedStatusView(LoginRequiredMixin, View):
    """
    Toggle the reviewed status of an application (True <-> False).
    """

    def post(self, request, *args, **kwargs):
        application_id = kwargs.get('pk')
        application = get_object_or_404(Application, pk=application_id)
        
        # Only managers or head managers can toggle the status
        user = request.user
        if not (user in application.vacancy.company.managers.all() or user == application.vacancy.company.head_manager):
            return redirect('manager_applications')
        
        # Toggle the reviewed status
        application.reviewed = not application.reviewed
        application.save()

        # Redirect to the list of applications
        return redirect('manager_applications')