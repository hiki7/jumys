import pytest
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_custom_token_obtain_pair_view(client, django_user_model):
    """Test the CustomTokenObtainPairView with valid credentials"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123', role='seeker')
    
    response = client.post(reverse('token_obtain_pair'), data={'username': 'testuser', 'password': 'testpass123'})
    
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_custom_token_obtain_pair_view_invalid_credentials(client, django_user_model):
    """Test the CustomTokenObtainPairView with invalid credentials"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123', role='seeker')
    
    response = client.post(reverse('token_obtain_pair'), data={'username': 'testuser', 'password': 'wrongpassword'})
    
    assert response.status_code == 401
    assert 'access' not in response.data
    assert 'refresh' not in response.data


@pytest.mark.django_db
def test_login_view_get_request(client):
    """Test the GET request for login view"""
    response = client.get(reverse('login'))
    
    assert response.status_code == 200
    assert 'Login' in response.content.decode()


@pytest.mark.django_db
def test_login_view_post_valid_credentials(client, django_user_model):
    """Test login view with valid credentials"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123', role='seeker')
    
    response = client.post(reverse('login'), data={'username': 'testuser', 'password': 'testpass123'})
    
    assert response.status_code == 302  # Should redirect on success
    assert response.url == reverse('home')  # Ensure it redirects to the home page


@pytest.mark.django_db
def test_login_view_post_invalid_credentials(client):
    """Test login view with invalid credentials"""
    response = client.post(reverse('login'), data={'username': 'wronguser', 'password': 'wrongpass'})
    
    assert response.status_code == 200  # Renders the form again
    assert 'Invalid credentials' in response.content.decode()


@pytest.mark.django_db
def test_register_view_get_request(client):
    """Test the GET request for register view"""
    response = client.get(reverse('register'))
    
    assert response.status_code == 200
    assert 'Register' in response.content.decode()


@pytest.mark.django_db
def test_register_view_post_valid_data(client, django_user_model):
    """Test registration form POST with valid data"""
    data = {
        'username': 'newuser',
        'password': 'password123',
        'role': 'seeker'
    }
    
    response = client.post(reverse('register'), data=data)
    
    assert response.status_code == 302  # Should redirect to login page
    assert CustomUser.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_register_view_post_invalid_role(client, django_user_model):
    """Test registration form POST with an invalid role"""
    data = {
        'username': 'newuser',
        'password': 'password123',
        'role': 'invalid_role'
    }
    
    response = client.post(reverse('register'), data=data)
    
    assert response.status_code == 200  # Re-renders the form
    assert 'Invalid role selected.' in response.content.decode()


@pytest.mark.django_db
def test_register_view_post_existing_username(client, django_user_model):
    """Test registration form POST with an existing username"""
    django_user_model.objects.create_user(username='newuser', password='password123', role='seeker')
    
    data = {
        'username': 'newuser',
        'password': 'password123',
        'role': 'seeker'
    }
    
    response = client.post(reverse('register'), data=data)
    
    assert response.status_code == 200  # Re-renders the form
    assert 'Username already taken.' in response.content.decode()
