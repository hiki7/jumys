# vacancies/urls.py

from django.urls import path
from .views import (
    VacancyListView,
    VacancyDetailView,
    VacancyCreateView,
    VacancyUpdateView,
    VacancyDeleteView,
    ApplyToVacancyView,
    BookmarkVacancyView
)

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancy_list'),  # List all vacancies
    path('create/', VacancyCreateView.as_view(), name='vacancy_create'),  # Create a new vacancy
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),  # Vacancy detail
    path('<int:pk>/update/', VacancyUpdateView.as_view(), name='vacancy_update'),  # Update vacancy
    path('<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete'),  # Delete vacancy
    path('<int:pk>/apply/', ApplyToVacancyView.as_view(), name='apply_to_vacancy'),  # Apply to vacancy
    path('<int:pk>/bookmark/', BookmarkVacancyView.as_view(), name='bookmark_vacancy'),  # Bookmark vacancy
]
