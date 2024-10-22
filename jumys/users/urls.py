from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ViewUser, UpdateUser, DeleteUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Profile-related URLs
    path('profile/', ViewUser, name='user_profile'),
    path('profile/update/', UpdateUser, name='update_user'),
    path('profile/delete/', DeleteUser, name='delete_user'),
]
