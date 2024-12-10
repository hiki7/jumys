import pytest
from django.urls import reverse, resolve
from seekers.views import (
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
from seekers.models import UserProfile, Ability, WorkExperience, Application
from vacancies.models import Vacancy
from users.models import CustomUser


@pytest.mark.django_db
class TestSeekersViews:

    @pytest.fixture
    def user(self, django_user_model):
        """Create and return a user, and ensure only one UserProfile is created"""
        user = django_user_model.objects.create_user(username='testuser', password='testpass123')
        # If UserProfile is automatically created, remove this line
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        return user

    def test_get_user_profile_detail_view(self, client, user):
        """Test GET request for UserProfileDetailView"""
        client.force_login(user)
        response = client.get(reverse('profile'))
        assert response.status_code == 200
        assert 'profile' in response.context

    def test_get_edit_profile_view(self, client, user):
        """Test GET request for EditProfileView"""
        client.force_login(user)
        response = client.get(reverse('profile_edit'))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_post_edit_profile_view(self, client, user):
        """Test POST request for EditProfileView to update profile"""
        client.force_login(user)
        data = {'phone': '123456789', 'links': 'https://example.com'}
        response = client.post(reverse('profile_edit'), data)
        user.profile.refresh_from_db()
        assert response.status_code == 302
        assert user.profile.phone == '123456789'

    def test_get_user_applied_vacancies_view(self, client, user):
        """Test GET request for UserAppliedVacanciesView"""
        client.force_login(user)
        response = client.get(reverse('applied_vacancies'))
        assert response.status_code == 200
        assert 'applications' in response.context

    def test_get_user_abilities_view(self, client, user):
        """Test GET request for UserAbilitiesView"""
        client.force_login(user)
        response = client.get(reverse('abilities'))
        assert response.status_code == 200
        assert 'abilities' in response.context

    def test_post_user_abilities_view(self, client, user):
        """Test POST request for UserAbilitiesView to add ability"""
        client.force_login(user)
        data = {'technology': 'Python', 'experience_years': 3, 'proficiency_level': 'senior'}
        response = client.post(reverse('abilities'), data)
        assert response.status_code == 302
        assert Ability.objects.filter(technology='Python').exists()

    def test_post_remove_ability_view(self, client, user):
        """Test POST request for RemoveAbilityView to remove an ability"""
        client.force_login(user)
        ability = Ability.objects.create(technology='Python', experience_years=3, proficiency_level='senior')
        user.profile.abilities.add(ability)
        response = client.post(reverse('remove_ability', kwargs={'ability_id': ability.id}))
        assert response.status_code == 302
        assert ability not in user.profile.abilities.all()

    def test_get_user_work_experience_view(self, client, user):
        """Test GET request for UserWorkExperienceView"""
        client.force_login(user)
        response = client.get(reverse('work_experience'))
        assert response.status_code == 200
        assert 'work_experience' in response.context



