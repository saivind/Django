from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser
from .forms import CreateUserForm
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):

    model = NewUser
    add_form = CreateUserForm
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff','is_manager','is_engineer')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'first_name',
                    'is_active', 'is_staff', 'is_manager','is_engineer')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_manager','is_engineer','groups', 'user_permissions',)}),
        #('Personal', {'fields': ('about',)}),
        
    )
	
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_staff','is_manager','is_engineer')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
