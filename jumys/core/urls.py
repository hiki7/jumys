from django.urls import path
from .views import home_view, login_view, register_view, profile_view, post_view, CompanyCreateTemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('post/', post_view, name='post'),
    path('company/create/', CompanyCreateTemplateView.as_view(), name='company_create'),  # Add this line
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]