from django.urls import path
from .views import VacancyListCreateView, VacancyDetailView

urlpatterns = [
    path('', VacancyListCreateView.as_view(), name='vacancy_list_create'),
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
]
