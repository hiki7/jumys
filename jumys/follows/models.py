from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f"{self.follower} follows {self.followee}"

class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connection_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connection_requests_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Connection from {self.sender} to {self.receiver}: {self.status}"

class ReferenceLetter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_letters_written')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_letters_received')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reference letter from {self.author} to {self.recipient}"
