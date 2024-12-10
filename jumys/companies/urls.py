from django.urls import path
from .views import (
    CreateCompanyHTMLView,
    CompanyDetailView,
    EditCompanyView,
    DeleteCompanyView,
    AddManagerView,
)

urlpatterns = [
    # HTML Views
    path('create/', CreateCompanyHTMLView.as_view(), name='create_company'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('<int:pk>/edit/', EditCompanyView.as_view(), name='edit_company'),
    path('<int:pk>/delete/', DeleteCompanyView.as_view(), name='delete_company'),

    # API Endpoints
    path('<int:company_id>/add_manager/', AddManagerView.as_view(), name='add_manager_to_company'),
]
