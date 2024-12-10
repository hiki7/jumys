import pytest
from django.urls import reverse, resolve
from users.views import login_view, register_view, CustomTokenObtainPairView, RegisterView
from django.contrib.auth.views import LogoutView


@pytest.mark.parametrize("url_name, view, kwargs", [
    ("login", login_view, None),
    ("register", register_view, None),
    ("token_obtain_pair", CustomTokenObtainPairView, None),
    ("api_register", RegisterView, None),
    ("logout", LogoutView, None),
])
def test_url_resolves_to_correct_view(url_name, view, kwargs):
    """Test that URL resolves to the correct view"""
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    resolved_view = resolve(url)
    if hasattr(view, 'as_view'):  # Check if it's a class-based view
        assert resolved_view.func.view_class == view
    else:  # Check if it's a function-based view
        assert resolved_view.func == view


@pytest.mark.parametrize("url_name, expected_path, kwargs", [
    ("login", "/api/users/login/", None),
    ("register", "/api/users/register/", None),
    ("token_obtain_pair", "/api/users/api/token/", None),
    ("api_register", "/api/users/api/register/", None),
    ("logout", "/api/users/logout/", None),
])
def test_url_reverse_generates_correct_path(url_name, expected_path, kwargs):
    """Test that reverse() returns the correct URL path"""
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    assert url == expected_path
