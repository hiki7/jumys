import pytest
from django.urls import reverse
from companies.models import Company, Country, City, Street, Location
from users.models import CustomUser


@pytest.mark.django_db
def test_create_company_view_get(client, django_user_model):
    """Test the GET request for the CreateCompanyHTMLView endpoint"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)
    response = client.get(reverse('create_company'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.templates[0].name == 'companies/create_company.html'

@pytest.mark.django_db
def test_company_detail_view(client, django_user_model):
    """Test the CompanyDetailView endpoint"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
    response = client.get(reverse('company_detail', kwargs={'pk': company.pk}))
    assert response.status_code == 200
    assert 'company' in response.context
    assert response.context['company'] == company


@pytest.mark.django_db
def test_edit_company_view_get(client, django_user_model):
    """Test the GET request for the EditCompanyView endpoint"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123', role='admin')
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
    """Test the DeleteCompanyView endpoint"""
    user = django_user_model.objects.create_user(username='adminuser', password='testpass123', role='admin')
    client.force_login(user)
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
    response = client.post(reverse('delete_company', kwargs={'pk': company.pk}))
    assert response.status_code == 302  # Redirect on success
    assert not Company.objects.filter(pk=company.pk).exists()  # Check if company was deleted


@pytest.mark.django_db
def test_add_manager_view_get(client, django_user_model):
    """Test the GET request for the AddManagerView endpoint"""
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.force_login(user)
    country = Country.objects.create(name='Kazakhstan')
    city = City.objects.create(name='Almaty', country=country)
    street = Street.objects.create(name='Main Street')
    location = Location.objects.create(country=country, city=city, street=street)
    company = Company.objects.create(name='Test Company', company_description='Test Description', location=location, head_manager=user)
    response = client.get(reverse('add_manager_to_company', kwargs={'company_id': company.pk}))
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'company' in response.context


