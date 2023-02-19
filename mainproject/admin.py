from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class User_Admin(UserAdmin):
    model = User
    list_display = ('iin', 'is_superuser','is_staff')
    list_filter = ('iin', 'is_superuser', 'first_name','last_name')
    fieldsets = (
        (None, {'fields': ('iin', 'password', 'first_name','last_name','email',)}),
        ('Права доступа и потверждение', {'fields': ('is_staff','is_superuser')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('iin', 'password1', 'password2', 'first_name','last_name','email',)},
            
        ),
         ('Права доступа и потверждение', {'fields': ('is_staff','is_superuser')}),
    )
    search_fields = ('iin',)
    ordering = ('iin',)


class Books_Admin(admin.ModelAdmin):
    model = Books
    list_display = ('name','photo','age','date_add')
    search_fields = ('name','photo','age','date_add')
    ordering = ('name','photo','age','date_add')


class Manager_Admin(admin.ModelAdmin):
    model = Manager
    list_display = ('user','book','Date_start','Date_end','commoner')
    search_fields = ('user','book','Date_start','Date_end','commoner','commoner_time')
    ordering = ('user','book','Date_start','Date_end','commoner','commoner_time')


class News_Admin(admin.ModelAdmin):
    model = News
    list_display = ('id','name','image',)
    search_fields = ('id','name','image',)
    ordering = ('id','name','image',)


admin.site.register(User,User_Admin)

admin.site.register(Manager,Manager_Admin)

admin.site.register(Books,Books_Admin)

admin.site.register(News,News_Admin)
