# urls.py
from django.urls import path
from .views import ProfileDeleteView, ProfileUpdateView, RegisterView,CustomLoginView,CustomLogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]
