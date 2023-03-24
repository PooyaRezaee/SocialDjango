from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'classes': ('tabular',),'fields': ('first_name', 'last_name','age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'classes': ('tabular',),'fields': ('last_login','date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined','last_login')
    
    list_display = ('username','email', 'first_name', 'last_name','age', 'is_staff')
    list_filter = ('date_joined',)
    search_fields = ('email','username','first_name','last_name')
    ordering = ('username','email',)
    filter_horizontal = ('groups', 'user_permissions')
