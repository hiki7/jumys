from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
# from . import api_views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]