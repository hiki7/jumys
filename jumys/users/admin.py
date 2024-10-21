from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_manager', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_manager')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    
    # Specify the fields to be displayed in the admin forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_manager')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_manager'),
        }),
    )

# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)