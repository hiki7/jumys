from django.urls import path
from .views import login_view, register_view, CustomTokenObtainPairView, RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    # Add other URL patterns as needed
]