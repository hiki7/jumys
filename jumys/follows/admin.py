from django.contrib import admin
from .models import Follow, Connection, ReferenceLetter

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followee', 'created_at')
    search_fields = ('follower__username', 'followee__username')
    list_filter = ('created_at',)

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at', 'updated_at')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('status', 'created_at')

@admin.register(ReferenceLetter)
class ReferenceLetterAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipient', 'status', 'created_at')
    search_fields = ('author__username', 'recipient__username', 'content')
    list_filter = ('status', 'created_at')
