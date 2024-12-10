from django.test import TestCase
from django.db.utils import IntegrityError
from users.models import CustomUser  # Update this import according to your project structure
from vacancies.models import Vacancy, Position  # Change this import to match your project structure
from companies.models import Company  # Change this import to match your project structure
from ...models import Ability, UserProfile, WorkExperience, Application  # Change 'your_app_name' to your app's name


class AbilityModelTest(TestCase):
    def test_create_ability(self):
        ability = Ability.objects.create(technology='Python', experience_years=5, proficiency_level='senior')
        self.assertEqual(ability.technology, 'Python')
        self.assertEqual(ability.experience_years, 5)
        self.assertEqual(ability.proficiency_level, 'senior')

    def test_unique_ability_constraint(self):
        Ability.objects.create(technology='Python', experience_years=5, proficiency_level='senior')
        with self.assertRaises(IntegrityError):
            Ability.objects.create(technology='Python', experience_years=5, proficiency_level='senior')

    def test_ability_str_method(self):
        ability = Ability.objects.create(technology='Python', experience_years=5, proficiency_level='senior')
        self.assertEqual(str(ability), 'Python - senior (5 years)')


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_one_to_one_relationship(self):
        """Ensure that a user can only have one UserProfile"""
        UserProfile.objects.create(user=self.user)
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(user=self.user)

    def test_user_profile_str_method(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), 'testuser@example.com')


class WorkExperienceModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.company = Company.objects.create(name='Test Company', company_description='Test Description')
        self.position = Position.objects.create(name='Software Engineer')

    def test_create_work_experience(self):
        work_experience = WorkExperience.objects.create(
            user_profile=self.user_profile,
            company=self.company,
            position=self.position,
            start_date='2022-01-01',
            end_date='2023-01-01',
            description='Worked on various development tasks.'
        )
        self.assertEqual(work_experience.user_profile, self.user_profile)
        self.assertEqual(work_experience.company, self.company)
        self.assertEqual(work_experience.position, self.position)
        self.assertEqual(work_experience.description, 'Worked on various development tasks.')

    def test_work_experience_many_to_many_abilities(self):
        """Test that abilities can be linked to work experience"""
        ability = Ability.objects.create(technology='Python', experience_years=5, proficiency_level='senior')
        work_experience = WorkExperience.objects.create(
            user_profile=self.user_profile,
            company=self.company,
            position=self.position,
            start_date='2022-01-01'
        )
        work_experience.abilities.add(ability)
        self.assertIn(ability, work_experience.abilities.all())

    def test_work_experience_str_method(self):
        work_experience = WorkExperience.objects.create(
            user_profile=self.user_profile,
            company=self.company,
            position=self.position,
            start_date='2022-01-01',
            end_date='2023-01-01'
        )
        self.assertEqual(str(work_experience), f"testuser@example.com - {self.company.name} ({self.position.name}) [Ended 2023-01-01]")

    def test_work_experience_ordering(self):
        """Test that work experiences are ordered by -start_date"""
        WorkExperience.objects.create(user_profile=self.user_profile, company=self.company, position=self.position, start_date='2021-01-01')
        latest_experience = WorkExperience.objects.create(user_profile=self.user_profile, company=self.company, position=self.position, start_date='2023-01-01')
        experiences = WorkExperience.objects.all()
        self.assertEqual(experiences.first(), latest_experience)


class ApplicationModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.company = Company.objects.create(name='Test Company', company_description='Test Description')
        self.position = Position.objects.create(name='Software Engineer')
        self.vacancy = Vacancy.objects.create(company=self.company, position_name='Software Engineer')

    def test_create_application(self):
        application = Application.objects.create(user_profile=self.user_profile, vacancy=self.vacancy)
        self.assertEqual(application.user_profile, self.user_profile)
        self.assertEqual(application.vacancy, self.vacancy)
        self.assertFalse(application.reviewed)

    def test_application_default_reviewed_value(self):
        """Test that the default value of 'reviewed' is False"""
        application = Application.objects.create(user_profile=self.user_profile, vacancy=self.vacancy)
        self.assertFalse(application.reviewed)

    def test_application_str_method(self):
        """Test that the __str__ method returns the correct format"""
        application = Application.objects.create(user_profile=self.user_profile, vacancy=self.vacancy)
        self.assertEqual(str(application), f"{self.user_profile.user.email} applied for {self.vacancy.position_name} at {self.vacancy.company.name}")

    def test_application_ordering(self):
        """Test that applications are ordered by -applied_on"""
        Application.objects.create(user_profile=self.user_profile, vacancy=self.vacancy, applied_on='2023-01-01 12:00:00')
        latest_application = Application.objects.create(user_profile=self.user_profile, vacancy=self.vacancy, applied_on='2023-02-01 12:00:00')
        applications = Application.objects.all()
        self.assertEqual(applications.first(), latest_application)
