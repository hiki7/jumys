import pytest
from django.urls import reverse, resolve
from vacancies.views import (
    VacancyListView,
    VacancyDetailView,
    VacancyCreateView,
    VacancyUpdateView,
    VacancyDeleteView,
    ApplyToVacancyView,
    BookmarkVacancyView,
    ManagerApplicationsView,
    ToggleReviewedStatusView,
)


# Test if URL resolves to the correct view
@pytest.mark.parametrize("url_name, view, kwargs", [
    ("vacancy_list", VacancyListView, None),
    ("vacancy_create", VacancyCreateView, None),
    ("vacancy_detail", VacancyDetailView, {'pk': 1}),
    ("vacancy_update", VacancyUpdateView, {'pk': 1}),
    ("vacancy_delete", VacancyDeleteView, {'pk': 1}),
    ("apply_to_vacancy", ApplyToVacancyView, {'pk': 1}),
    ("bookmark_vacancy", BookmarkVacancyView, {'pk': 1}),
    ("manager_applications", ManagerApplicationsView, None),
    ("toggle_reviewed", ToggleReviewedStatusView, {'pk': 1}),
])
def test_url_resolves_to_view(url_name, view, kwargs):
    """Test that URL resolves to the correct view"""
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    assert resolve(url).func.view_class == view


@pytest.mark.parametrize("url_name, expected_path, kwargs", [
    ("vacancy_list", "/api/vacancies/", None),
    ("vacancy_create", "/api/vacancies/create/", None),
    ("vacancy_detail", "/api/vacancies/1/", {'pk': 1}),
    ("vacancy_update", "/api/vacancies/1/update/", {'pk': 1}),
    ("vacancy_delete", "/api/vacancies/1/delete/", {'pk': 1}),
    ("apply_to_vacancy", "/api/vacancies/1/apply/", {'pk': 1}),
    ("bookmark_vacancy", "/api/vacancies/1/bookmark/", {'pk': 1}),
    ("manager_applications", "/api/vacancies/manager/applications/", None),
    ("toggle_reviewed", "/api/vacancies/manager/applications/toggle-reviewed/1/", {'pk': 1}),
])
def test_url_reverse_matches_expected_path(url_name, expected_path, kwargs):
    """Test that reverse() returns the correct URL path"""
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    assert url == expected_path
