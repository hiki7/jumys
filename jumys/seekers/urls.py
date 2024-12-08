from django.urls import path
from .views import (
    UserProfileDetailView,
    UserAppliedVacanciesView,
    UserBookmarkedVacanciesView,
    UserAbilitiesView,
    RemoveAbilityView,
    UserWorkExperienceView,
    ManageWorkExperienceView,
)

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='user_profile'),
    path('profile/applied-vacancies/', UserAppliedVacanciesView.as_view(), name='user_applied_vacancies'),
    path('profile/bookmarked-vacancies/', UserBookmarkedVacanciesView.as_view(), name='user_bookmarked_vacancies'),
    path(
        'profile/bookmarked-vacancies/<int:vacancy_id>/',
        UserBookmarkedVacanciesView.as_view(),
        name='user_unbookmark_vacancy'
    ),
    path('profile/abilities/', UserAbilitiesView.as_view(), name='user_abilities'),
    path(
        'profile/abilities/<int:ability_id>/remove/',
        RemoveAbilityView.as_view(),
        name='user_remove_ability'
    ),
    path('profile/work-experience/', UserWorkExperienceView.as_view(), name='user_work_experience'),
    path(
        'profile/work-experience/<int:pk>/',
        ManageWorkExperienceView.as_view(),
        name='user_manage_work_experience'
    ),
]
