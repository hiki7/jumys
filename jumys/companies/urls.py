from django.urls import path
from .views import (
    CompanyListView,
    CreateCompanyHTMLView,
    CompanyDetailView,
    EditCompanyView,
    DeleteCompanyView,
    AddManagerView,
)
from rest_framework.routers import DefaultRouter
from .api_views import CountryViewSet, CityViewSet, StreetViewSet, LocationViewSet, CompanyViewSet

# Create the router and register your DRF viewsets
router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'streets', StreetViewSet, basename='street')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'companies', CompanyViewSet, basename='company')

# Combine router URLs with your existing urlpatterns
urlpatterns = router.urls + [
    # HTML Views
    path('create/', CreateCompanyHTMLView.as_view(), name='create_company'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('<int:pk>/edit/', EditCompanyView.as_view(), name='edit_company'),
    path('<int:pk>/delete/', DeleteCompanyView.as_view(), name='delete_company'),
    path('list/', CompanyListView.as_view(), name='company_list'),
    # Additional API Endpoint
    path('<int:company_id>/add_manager/', AddManagerView.as_view(), name='add_manager_to_company'),
]
