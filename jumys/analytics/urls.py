from django.urls import path
from .views import (
    user_role_distribution, 
    user_login_activity, 
    applications_per_vacancy,
    abilities_distribution,
    analytics_home,
    vacancies_per_day
)

urlpatterns = [
    path('', analytics_home, name='analytics_home'),
    path('users/role-distribution/', user_role_distribution, name='user_role_distribution'),
    path('users/login-activity/', user_login_activity, name='user_login_activity'),
    path('vacancies/applications/', applications_per_vacancy, name='applications_per_vacancy'),
    path('abilities/distribution/', abilities_distribution, name='abilities_distribution'),
    path('vacancies/per-day/', vacancies_per_day, name='vacancies_per_day'),
]
