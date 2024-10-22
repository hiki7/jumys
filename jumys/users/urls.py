from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, view_user_view, delete_user_view, update_user_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Profile-related URLs
    path('profile/', view_user_view, name='user_profile'),
    path('profile/update/', update_user_view, name='update_user'),
    path('profile/delete/', delete_user_view, name='delete_user'),
]
