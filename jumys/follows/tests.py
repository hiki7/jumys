from django.test import TestCase
from django.db.utils import IntegrityError
from users.models import CustomUser  # Update this import according to your project structure
from .models import Follow, Connection, ReferenceLetter  # Change 'your_app_name' to your app's name


class FollowModelTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='testpassword')
        self.user2 = CustomUser.objects.create_user(username='user2', password='testpassword')

    def test_create_follow(self):
        follow = Follow.objects.create(follower=self.user1, followee=self.user2)
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.followee, self.user2)
    
    def test_unique_follow_constraint(self):
        """Test that a follower cannot follow the same user twice"""
        Follow.objects.create(follower=self.user1, followee=self.user2)
        with self.assertRaises(IntegrityError):
            Follow.objects.create(follower=self.user1, followee=self.user2)

    def test_follow_str_method(self):
        follow = Follow.objects.create(follower=self.user1, followee=self.user2)
        self.assertEqual(str(follow), f"{self.user1} follows {self.user2}")


class ConnectionModelTest(TestCase):
    def setUp(self):
        self.sender = CustomUser.objects.create_user(username='sender', password='testpassword')
        self.receiver = CustomUser.objects.create_user(username='receiver', password='testpassword')

    def test_create_connection(self):
        connection = Connection.objects.create(sender=self.sender, receiver=self.receiver)
        self.assertEqual(connection.sender, self.sender)
        self.assertEqual(connection.receiver, self.receiver)
        self.assertEqual(connection.status, 'pending')  # Default status should be 'pending'

    def test_unique_connection_constraint(self):
        """Test that a sender cannot send the same connection request to the same user twice"""
        Connection.objects.create(sender=self.sender, receiver=self.receiver)
        with self.assertRaises(IntegrityError):
            Connection.objects.create(sender=self.sender, receiver=self.receiver)
    
    def test_connection_default_status(self):
        """Test that the default status of a connection is 'pending'"""
        connection = Connection.objects.create(sender=self.sender, receiver=self.receiver)
        self.assertEqual(connection.status, 'pending')

    def test_connection_status_update(self):
        """Test that updating the connection status works as expected"""
        connection = Connection.objects.create(sender=self.sender, receiver=self.receiver)
        connection.status = 'accepted'
        connection.save()
        self.assertEqual(connection.status, 'accepted')

    def test_connection_str_method(self):
        """Test that the __str__ method returns the correct format"""
        connection = Connection.objects.create(sender=self.sender, receiver=self.receiver)
        self.assertEqual(str(connection), f"Connection from {self.sender} to {self.receiver}: pending")


class ReferenceLetterModelTest(TestCase):
    def setUp(self):
        self.author = CustomUser.objects.create_user(username='author', password='testpassword')
        self.recipient = CustomUser.objects.create_user(username='recipient', password='testpassword')

    def test_create_reference_letter(self):
        """Test that a reference letter can be created successfully"""
        reference_letter = ReferenceLetter.objects.create(
            author=self.author,
            recipient=self.recipient,
            content="This is a reference letter."
        )
        self.assertEqual(reference_letter.author, self.author)
        self.assertEqual(reference_letter.recipient, self.recipient)
        self.assertEqual(reference_letter.content, "This is a reference letter.")
        self.assertEqual(reference_letter.status, 'pending')  # Default status should be 'pending'

    def test_reference_letter_default_status(self):
        """Test that the default status of a reference letter is 'pending'"""
        reference_letter = ReferenceLetter.objects.create(
            author=self.author,
            recipient=self.recipient,
            content="This is a reference letter."
        )
        self.assertEqual(reference_letter.status, 'pending')

    def test_reference_letter_status_update(self):
        """Test that the status of a reference letter can be updated successfully"""
        reference_letter = ReferenceLetter.objects.create(
            author=self.author,
            recipient=self.recipient,
            content="This is a reference letter."
        )
        reference_letter.status = 'accepted'
        reference_letter.save()
        self.assertEqual(reference_letter.status, 'accepted')

    def test_reference_letter_str_method(self):
        """Test that the __str__ method returns the correct format"""
        reference_letter = ReferenceLetter.objects.create(
            author=self.author,
            recipient=self.recipient,
            content="This is a reference letter."
        )
        self.assertEqual(str(reference_letter), f"Reference letter from {self.author} to {self.recipient}")
