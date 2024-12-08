from rest_framework import serializers
from .models import Follow, Connection, ReferenceLetter

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee', 'created_at']

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']

class ReferenceLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceLetter
        fields = ['id', 'author', 'recipient', 'content', 'status', 'created_at']
        read_only_fields = ['author', 'status', 'created_at', 'updated_at']
