from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'role', 'is_active', 'profile_picture')
    list_filter = ('is_staff', 'is_active', 'role')
    
    # Organizing fields into sections 
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'profile_picture')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined',)}),
    )

    # Form for adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
    # Setting read-only fields
    readonly_fields = ('date_joined', 'last_login')

    # Fields used for listing and ordering users
    search_fields = ('email', 'username', 'role')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)