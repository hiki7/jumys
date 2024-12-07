# core/urls.py

from django.urls import path
from .views import (
    home_view, login_view, register_view, profile_view, post_view, 
    CreateCompanyHTMLView, CompanyDetailView, EditCompanyView, DeleteCompanyView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('post/', post_view, name='post'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Company URLs
    path('companies/create/', CreateCompanyHTMLView.as_view(), name='create_company'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('companies/<int:pk>/edit/', EditCompanyView.as_view(), name='edit_company'),
    path('companies/<int:pk>/delete/', DeleteCompanyView.as_view(), name='delete_company'),
]
