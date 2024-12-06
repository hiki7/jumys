from django.urls import path
from .views import UserProfileView, ApplyToVacancyView, BookmarkVacancyView, AbilityListCreateView, WorkExperienceListCreateView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('apply/<int:vacancy_id>/', ApplyToVacancyView.as_view(), name='apply_to_vacancy'),
    path('bookmark/<int:vacancy_id>/', BookmarkVacancyView.as_view(), name='bookmark_vacancy'),
    path('abilities/', AbilityListCreateView.as_view(), name='ability_list_create'),
    path('work-experience/', WorkExperienceListCreateView.as_view(), name='work_experience_list_create'),
]
