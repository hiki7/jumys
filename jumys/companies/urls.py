from django.urls import path
from .views import CompanyCreateView, AddManagerToCompanyView

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('<int:company_id>/add_manager/', AddManagerToCompanyView.as_view(), name='add_manager_to_company'),
]
