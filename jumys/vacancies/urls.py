from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('vacancy/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancy/<int:pk>/delete/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('vacancy/<int:pk>/update/', views.VacancyUpdateView.as_view(), name='vacancy_update'),
    path('vacancy/create/', views.VacancyCreateView.as_view(), name='vacancy_create'),
]