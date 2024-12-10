import pytest
from django.urls import reverse
from django.db.utils import IntegrityError
from users.models import CustomUser
from companies.models import Company, Location, Country, City
from vacancies.models import Position, EmploymentType, Technology, Vacancy
from seekers.models import UserProfile


@pytest.fixture
def setup_data(db):
    """Fixture to set up shared test data"""
    user = CustomUser.objects.create_user(username='testuser', password='testpass123')
    country = Country.objects.create(name="Kazakhstan")
    city = City.objects.create(name="Almaty", country=country)
    location = Location.objects.create(country=country, city=city)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location)
    position = Position.objects.create(name='Software Engineer')

    return {
        'user': user,
        'country': country,
        'city': city,
        'location': location,
        'company': company,
        'position': position
    }


@pytest.mark.django_db
def test_vacancy_detail_view(client, setup_data):
    """Test the VacancyDetailView"""
    user = setup_data['user']
    client.force_login(user)
    
    vacancy = Vacancy.objects.create(
        position_name=setup_data['position'], 
        company=setup_data['company'], 
        location=setup_data['location'], 
        is_active=True
    )
    
    response = client.get(reverse('vacancy_detail', kwargs={'pk': vacancy.pk}))
    assert response.status_code == 200
    assert 'vacancy' in response.context
    assert response.context['vacancy'] == vacancy


@pytest.mark.django_db
def test_vacancy_create_view_post_valid(client, setup_data):
    """Test VacancyCreateView with valid POST data"""
    user = setup_data['user']
    client.force_login(user)
    
    data = {
        'position_name': setup_data['position'].id,  # Position is a ForeignKey
        'company': setup_data['company'].id,  # Company is a ForeignKey
        'location': setup_data['location'].id,  # Location is a ForeignKey
        'salary_start': 50000,
        'salary_end': 100000,
        'currency': 'USD',
        'is_active': True
    }
    
    response = client.post(reverse('vacancy_create'), data)
    assert response.status_code == 302  # Redirect on success


@pytest.mark.django_db
def test_vacancy_update_view_post(client, setup_data):
    """Test VacancyUpdateView with valid POST data"""
    user = setup_data['user']
    client.force_login(user)
    
    vacancy = Vacancy.objects.create(
        position_name=setup_data['position'], 
        company=setup_data['company'], 
        location=setup_data['location'], 
        is_active=True
    )

    data = {
        'position_name': setup_data['position'].id,
        'company': setup_data['company'].id,
        'salary_start': 60000,
        'salary_end': 120000,
    }
    
    response = client.post(reverse('vacancy_update', kwargs={'pk': vacancy.pk}), data)
    assert response.status_code == 302  # Redirect on success


@pytest.mark.django_db
def test_vacancy_delete_view_post(client, setup_data):
    """Test the VacancyDeleteView"""
    user = setup_data['user']
    user.role = 'admin'  # Assign the admin role to ensure the user has permission to delete
    user.save()
    client.force_login(user)
    
    vacancy = Vacancy.objects.create(
        position_name=setup_data['position'], 
        company=setup_data['company'], 
        location=setup_data['location'], 
        is_active=True
    )

    response = client.post(reverse('vacancy_delete', kwargs={'pk': vacancy.pk}))
    assert response.status_code == 302  # Check for redirection after deletion
    assert not Vacancy.objects.filter(pk=vacancy.pk).exists()  # Ensure the vacancy is deleted


@pytest.mark.django_db
def test_apply_to_vacancy_view_post(client, setup_data):
    """Test the ApplyToVacancyView"""
    user = setup_data['user']
    UserProfile.objects.get_or_create(user=user)  # Ensure only one UserProfile exists
    client.force_login(user)
    
    vacancy = Vacancy.objects.create(
        position_name=setup_data['position'], 
        company=setup_data['company'], 
        location=setup_data['location'], 
        is_active=True
    )
    
    response = client.post(reverse('apply_to_vacancy', kwargs={'pk': vacancy.pk}))
    assert response.status_code == 302  # Redirect on success



