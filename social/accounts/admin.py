from typing import Any
from django.contrib import admin
from .forms import UserChangeForm, UserCreateForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OtpCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ['phone', 'email', 'created', 'is_admin']
    list_filter = ['is_superuser', 'is_admin', 'is_active']
    ordering = ['phone']
    search_fields = ['phone']
   
    fieldsets= [
        ('User information', {'fields':['phone', 'email', 'fullname', 'password', 'last_login', 'groups', 'user_permissions']}),
        ('Permissions', {'fields':['is_superuser', 'is_admin', 'is_active']}),
    ]
    
    add_fieldsets = [
        ('User information', {'fields':['phone', 'email', 'fullname', 'password1', 'password2', 'last_login']}),
        ('Permissions', {'fields':['is_superuser', 'is_admin']}),
    ]

    
   
    filter_horizontal = ['user_permissions', 'groups']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser: 
          form.base_fields['is_superuser'].disabled = True
        return form
    
admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)