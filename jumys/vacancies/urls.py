from django.urls import path
from .views import (VacancyListView, VacancyDetailView, VacancyCreateView,
                    VacancyUpdateView, VacancyDeleteView, hide_vacancy, hidden_vacancies, CompanyListView)

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancy_list'),
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('create/', VacancyCreateView.as_view(), name='vacancy_create'),
    path('<int:pk>/edit/', VacancyUpdateView.as_view(), name='vacancy_update'),
    path('<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('hide/<int:pk>/', hide_vacancy, name='hide_vacancy'),
    path('hidden-vacancies/', hidden_vacancies, name='hidden_vacancies'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
]
