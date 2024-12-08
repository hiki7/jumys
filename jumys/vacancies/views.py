from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsSeeker, IsAdminOrHR
from .models import Vacancy
from seekers.models import Application
from .forms import VacancyForm


# Helper to check permissions
def check_permission(user, permission_class):
    permission = permission_class()
    if not permission.has_permission(None, None):
        raise PermissionDenied


# Vacancy Views
class VacancyListView(ListView):
    model = Vacancy
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        return Vacancy.objects.filter(is_active=True)


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"


class VacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    success_url = reverse_lazy("vacancy_list")

    def dispatch(self, request, *args, **kwargs):
        check_permission(request.user, IsAdminOrHR)
        return super().dispatch(request, *args, **kwargs)


class VacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    success_url = reverse_lazy("vacancy_list")

    def dispatch(self, request, *args, **kwargs):
        check_permission(request.user, IsAdminOrHR)
        return super().dispatch(request, *args, **kwargs)


class VacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacancy
    template_name = "vacancies/vacancy_confirm_delete.html"
    success_url = reverse_lazy("vacancy_list")

    def dispatch(self, request, *args, **kwargs):
        check_permission(request.user, IsAdminOrHR)
        return super().dispatch(request, *args, **kwargs)


# Application Views
class ApplyToVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = "vacancies/apply_vacancy.html"

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()
        user_profile = request.user.profile

        if not vacancy.is_active:
            return render(
                request,
                "vacancies/error.html",
                {"message": "Vacancy does not exist or is inactive."},
            )

        if Application.objects.filter(user_profile=user_profile, vacancy=vacancy).exists():
            return render(
                request,
                "vacancies/error.html",
                {"message": "You have already applied to this vacancy."},
            )

        Application.objects.create(user_profile=user_profile, vacancy=vacancy)
        return redirect("vacancy_list")


class BookmarkVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = "vacancies/bookmark_vacancy.html"

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()

        if not vacancy.is_active:
            return render(
                request,
                "vacancies/error.html",
                {"message": "Vacancy does not exist or is inactive."},
            )

        if vacancy.bookmarked_by.filter(id=request.user.id).exists():
            return render(
                request,
                "vacancies/error.html",
                {"message": "Vacancy is already bookmarked."},
            )

        vacancy.bookmarked_by.add(request.user)
        return redirect("vacancy_list")

    def delete(self, request, *args, **kwargs):
        vacancy = self.get_object()

        if not vacancy.bookmarked_by.filter(id=request.user.id).exists():
            return render(
                request,
                "vacancies/error.html",
                {"message": "Vacancy is not bookmarked."},
            )

        vacancy.bookmarked_by.remove(request.user)
        return redirect("vacancy_list")
