from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    """Custom admin for CustomUser model"""
    
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_email_verified', 'is_active', 'is_staff']
    list_filter = ['role', 'is_email_verified', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'is_email_verified', 'email_verification_token')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'email')}),
    )


class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model"""
    
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'bio']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
