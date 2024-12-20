from django.urls import path
from .views import (
    UserProfileDetailView,
    EditProfileView,
    UserAppliedVacanciesView,
    UserBookmarkedVacanciesView,
    UserAbilitiesView,
    RemoveAbilityView,
    UserWorkExperienceView,
    ManageWorkExperienceView,
    DeleteWorkExperienceView
)


from rest_framework.routers import DefaultRouter
from .api_views import AbilityViewSet, UserProfileViewSet, WorkExperienceViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'abilities', AbilityViewSet, basename='ability')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'workexperiences', WorkExperienceViewSet, basename='workexperience')
router.register(r'applications', ApplicationViewSet, basename='application')


urlpatterns = router.urls +[
    path('profile/', UserProfileDetailView.as_view(), name='profile'),

    path('profile/<int:user_id>/', UserProfileDetailView.as_view(), name='profile'),
    path('profile/edit', EditProfileView.as_view(), name='profile_edit'),
    path('profile/applied-vacancies/', UserAppliedVacanciesView.as_view(), name='applied_vacancies'),
    path('profile/bookmarked-vacancies/', UserBookmarkedVacanciesView.as_view(), name='bookmarked_vacancies'),
    path('profile/bookmarked-vacancies/<int:vacancy_id>/', UserBookmarkedVacanciesView.as_view(), name='unbookmark_vacancy'),
    path('profile/abilities/', UserAbilitiesView.as_view(), name='abilities'),
    path('profile/abilities/<int:ability_id>/remove/', RemoveAbilityView.as_view(), name='remove_ability'),
    path('profile/work-experience/', UserWorkExperienceView.as_view(), name='work_experience'),
    path('profile/work-experience/<int:work_experience_id>/', ManageWorkExperienceView.as_view(), name='manage_work_experience'),
    path('profile/work-experience/<int:work_experience_id>/delete/', DeleteWorkExperienceView.as_view(), name='delete_work_experience'),
]
