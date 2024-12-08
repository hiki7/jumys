from django.urls import path
from .views import (
    UserProfileDetailView,
    UserAppliedVacanciesView,
    UserBookmarkedVacanciesView,
    UserUnbookmarkVacancyView,
    UserAbilitiesView,
    RemoveAbilityView,
    UserWorkExperienceView,
    ManageWorkExperienceView,
)

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='user_profile'),
    path('profile/applied-vacancies/', UserAppliedVacanciesView.as_view(), name='applied_vacancies'),
    path('profile/bookmarked-vacancies/', UserBookmarkedVacanciesView.as_view(), name='bookmarked_vacancies'),
    path('profile/bookmarked-vacancies/<int:vacancy_id>/unbookmark/', UserUnbookmarkVacancyView.as_view(),
         name='unbookmark_vacancy'),
    path('profile/abilities/', UserAbilitiesView.as_view(), name='abilities_list_create'),
    path('profile/abilities/<int:ability_id>/', RemoveAbilityView.as_view(), name='remove_ability'),
    path('profile/work-experience/', UserWorkExperienceView.as_view(), name='work_experience_list_create'),
    path('profile/work-experience/<int:pk>/', ManageWorkExperienceView.as_view(), name='manage_work_experience'),
]
