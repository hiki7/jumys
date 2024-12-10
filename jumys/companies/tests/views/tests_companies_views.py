import pytest
from django.urls import reverse
from companies.models import Company, Country, City, Street, Location


@pytest.mark.django_db
def test_create_company_get_view(client, django_user_model):
    """Test GET request to create company page"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)  # Login before making the request
    response = client.get(reverse('create_company'))
    assert response.status_code == 200  # The response should now be 200, not 302
    assert 'form' in response.context  # Check if the form exists in the context
    assert response.templates[0].name == 'companies/create_company.html'  # Template check



@pytest.mark.django_db
def test_create_company_post_invalid_data(client, django_user_model):
    """Test POST request with missing required fields"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)
    data = {'name': '', 'company_description': ''}
    response = client.post(reverse('create_company'), data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors

import pytest
from django.urls import reverse
from companies.models import Company, Country, City, Street, Location


@pytest.mark.django_db
def test_get_company_detail_view(client, django_user_model):
    """Test GET request for the company detail view"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
    response = client.get(reverse('company_detail', kwargs={'pk': company.pk}))
    assert response.status_code == 200
    assert response.templates[0].name == 'companies/company_detail.html'
    assert response.context['company'] == company

import pytest
from django.urls import reverse
from companies.models import Company, Country, City, Street, Location
from users.models import CustomUser


@pytest.mark.django_db
def test_get_add_manager_view_authenticated_user(client):
    """Test GET request for authenticated user"""
    user = CustomUser.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='This is a test description', location=location, head_manager=user)
    response = client.get(reverse('add_manager_to_company', kwargs={'company_id': company.id}))
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'company' in response.context
    assert response.context['company'] == company

@pytest.mark.django_db
def test_post_add_manager_view_with_invalid_company_id(client, django_user_model):
    """Test POST request with invalid company id"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)
    response = client.post(reverse('add_manager_to_company', kwargs={'company_id': 999}), {'user': [user.id]})
    assert response.status_code == 404

import pytest
from django.urls import reverse
from companies.models import Company, Country, City, Street, Location
from users.models import CustomUser


@pytest.mark.django_db
def test_edit_company_view(client, django_user_model):
    """Test GET request for edit company view"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
    response = client.get(reverse('edit_company', kwargs={'pk': company.pk}))
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.templates[0].name == 'companies/edit_company.html'


@pytest.mark.django_db
def test_delete_company_view(client, django_user_model):
    """Test that a company can be deleted"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123', role='admin')
    client.force_login(user)
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
    response = client.post(reverse('delete_company', kwargs={'pk': company.pk}))
    assert response.status_code == 302
    assert not Company.objects.filter(pk=company.pk).exists()
