from django.test import TestCase
from django.db.utils import IntegrityError
from users.models import CustomUser  # Update this import according to your project structure
from companies.models import Company, Location  # Change this import to match your project structure
from vacancies.models import Position, EmploymentType, Technology, Vacancy  # Change 'your_app_name' to your app's name
from companies.models import Country,City

class PositionModelTest(TestCase):
    def test_create_position(self):
        position = Position.objects.create(name='Software Engineer')
        self.assertEqual(position.name, 'Software Engineer')

    def test_unique_position_name(self):
        """Test that position names are unique"""
        Position.objects.create(name='Software Engineer')
        with self.assertRaises(IntegrityError):
            Position.objects.create(name='Software Engineer')

    def test_position_str_method(self):
        position = Position.objects.create(name='Software Engineer')
        self.assertEqual(str(position), 'Software Engineer')


class EmploymentTypeModelTest(TestCase):
    def test_create_employment_type(self):
        employment_type = EmploymentType.objects.create(name='Full-time')
        self.assertEqual(employment_type.name, 'Full-time')

    def test_unique_employment_type_name(self):
        """Test that employment type names are unique"""
        EmploymentType.objects.create(name='Full-time')
        with self.assertRaises(IntegrityError):
            EmploymentType.objects.create(name='Full-time')

    def test_employment_type_str_method(self):
        employment_type = EmploymentType.objects.create(name='Part-time')
        self.assertEqual(str(employment_type), 'Part-time')


class TechnologyModelTest(TestCase):
    def test_create_technology(self):
        technology = Technology.objects.create(technology_name='Python')
        self.assertEqual(technology.technology_name, 'Python')

    def test_unique_technology_name(self):
        """Test that technology names are unique"""
        Technology.objects.create(technology_name='Python')
        with self.assertRaises(IntegrityError):
            Technology.objects.create(technology_name='Python')

    def test_technology_str_method(self):
        technology = Technology.objects.create(technology_name='JavaScript')
        self.assertEqual(str(technology), 'JavaScript')



class VacancyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Shared data for all test methods"""
        # Create user for ManyToMany field
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        
        # Create Country and City objects
        cls.country = Country.objects.create(name="Kazakhstan")
        cls.city = City.objects.create(name="Almaty", country=cls.country)
        
        # Create Location object
        cls.location = Location.objects.create(country=cls.country, city=cls.city)
        
        # Create Company and link it to the Location
        cls.company = Company.objects.create(
            name='Test Company', 
            company_description='Test Description', 
            location=cls.location
        )
        
        # Create Position object
        cls.position = Position.objects.create(name='Software Engineer')

    def test_create_vacancy(self):
        """Test that a Vacancy can be created successfully"""
        vacancy = Vacancy.objects.create(
            position_name=self.position,
            company=self.company,
            location=self.location,
            salary_start=50000,
            salary_end=100000,
            currency='USD'
        )
        self.assertEqual(vacancy.position_name, self.position)
        self.assertEqual(vacancy.company, self.company)
        self.assertEqual(vacancy.location, self.location)
        self.assertEqual(vacancy.salary_start, 50000)
        self.assertEqual(vacancy.salary_end, 100000)
        self.assertEqual(vacancy.currency, 'USD')

    def test_default_currency_is_kzt(self):
        """Test that the default currency for a Vacancy is 'KZT'"""
        vacancy = Vacancy.objects.create(
            position_name=self.position,
            company=self.company,
            location=self.location
        )
        self.assertEqual(vacancy.currency, 'KZT')

    def test_vacancy_is_active_by_default(self):
        """Test that the default value for is_active is True"""
        vacancy = Vacancy.objects.create(
            position_name=self.position,
            company=self.company,
            location=self.location
        )
        self.assertTrue(vacancy.is_active)

    def test_vacancy_str_method(self):
        """Test that the __str__ method returns the correct format"""
        vacancy = Vacancy.objects.create(
            position_name=self.position,
            company=self.company,
            location=self.location
        )
        self.assertEqual(str(vacancy), f"{self.position.name} at {self.company.name}")