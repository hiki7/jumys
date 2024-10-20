from django.urls import path
from .views import (
    UserProfileCreateView,
    UserProfileUpdateView,
    remove_ability,
    AbilityCreateView,
    WorkExperienceCreateView,
    WorkExperienceUpdateView,
    WorkExperienceDeleteView,
    ApplicationListView,
    ApplicationDeleteView
)

urlpatterns = [
    path('profile/create/', UserProfileCreateView.as_view(), name='userprofile_create'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='userprofile_update'),
    path('profile/remove-ability/<int:ability_id>/', remove_ability, name='remove_ability'),

    path('ability/add/', AbilityCreateView.as_view(), name='ability_create'),

    path('work-experience/add/', WorkExperienceCreateView.as_view(), name='workexperience_create'),
    path('work-experience/update/<int:pk>/', WorkExperienceUpdateView.as_view(), name='workexperience_update'),
    path('work-experience/delete/<int:pk>/', WorkExperienceDeleteView.as_view(), name='workexperience_delete'),

    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/delete/<int:pk>/', ApplicationDeleteView.as_view(), name='application_delete'),
]
