from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

# Register your models here.
class UserAcountAdmin(UserAdmin):
    list_display = ['id','email','first_name','username','last_login','date_joined']
    list_display_links =['first_name','email']
    readonly_fields = ('last_login','date_joined',)
    ordering = ('-date_joined',)

    filter_horizontal=()
    list_filter =()

    fieldsets=[
        ('User credential', {'fields':['email','password']}),
        ('Personal Info',{'fields':['username','first_name','last_name','phone_no']}),
        ('permissons',{'fields':['is_admin','is_active','is_staff','is_superadmin']}),
    ]

    add_fieldsets=[
        (None,
         {
             'classes':['wide'],
             'fields':['email','username','first_name','last_name','password','password2']
         })
    ]

admin.site.register(UserAccount,UserAcountAdmin)