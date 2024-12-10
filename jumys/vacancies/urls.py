from django.urls import path
from .views import  VacancyDetailView, ApplyToVacancyView, BookmarkVacancyView

urlpatterns = [
    #path('', VacancyListCreateView.as_view(), name='vacancy_list_create'),
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('<int:vacancy_id>/apply/', ApplyToVacancyView.as_view(), name='apply_to_vacancy'),
    path('<int:vacancy_id>/bookmark/', BookmarkVacancyView.as_view(), name='bookmark_vacancy')
]
