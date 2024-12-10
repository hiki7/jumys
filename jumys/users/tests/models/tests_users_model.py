from django.test import TestCase
from users.models import CustomUser  # Change 'users' to the name of your app where CustomUser is located


class CustomUserModelTest(TestCase):
    def test_create_custom_user(self):
        """Test that a CustomUser can be created successfully"""
        user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_default_role_is_seeker(self):
        """Test that the default role of a new user is 'seeker'"""
        user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.assertEqual(user.role, 'seeker')

    def test_user_can_have_role_hr(self):
        """Test that a user can be assigned the role of 'hr'"""
        user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com', role='hr')
        self.assertEqual(user.role, 'hr')

    def test_user_can_have_role_admin(self):
        """Test that a user can be assigned the role of 'admin'"""
        user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com', role='admin')
        self.assertEqual(user.role, 'admin')

    def test_user_str_method(self):
        """Test the __str__ method returns the correct string format"""
        user = CustomUser.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.assertEqual(str(user), 'testuser')
