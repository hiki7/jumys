# vacancies/urls.py

from django.urls import path
from .views import (
    ManagerApplicationsView,
    ToggleReviewedStatusView,
    VacancyListView,
    VacancyDetailView,
    VacancyCreateView,
    VacancyUpdateView,
    VacancyDeleteView,
    ApplyToVacancyView,
    BookmarkVacancyView
)
from rest_framework.routers import DefaultRouter
from .api_views import PositionViewSet, EmploymentTypeViewSet, TechnologyViewSet, VacancyViewSet

router = DefaultRouter()
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'employmenttypes', EmploymentTypeViewSet, basename='employmenttype')
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'vacancies', VacancyViewSet, basename='vacancy')


urlpatterns = router.urls + [
    path('list/', VacancyListView.as_view(), name='vacancy_list'),  # List all vacancies
    path('create/', VacancyCreateView.as_view(), name='vacancy_create'),  # Create a new vacancy
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),  # Vacancy detail
    path('<int:pk>/update/', VacancyUpdateView.as_view(), name='vacancy_update'),  # Update vacancy
    path('<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete'),  # Delete vacancy
    path('<int:pk>/apply/', ApplyToVacancyView.as_view(), name='apply_to_vacancy'),  # Apply to vacancy
    path('<int:pk>/bookmark/', BookmarkVacancyView.as_view(), name='bookmark_vacancy'),  # Bookmark vacancy
    path('manager/applications/', ManagerApplicationsView.as_view(), name='manager_applications'),
    path('manager/applications/toggle-reviewed/<int:pk>/', ToggleReviewedStatusView.as_view(), name='toggle_reviewed'),

]
