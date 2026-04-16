from django.contrib import admin
from .models import AddTask

# Register your models here.
class AddTaskAdmin(admin.ModelAdmin):
    list_display = ['user','title',]


admin.site.register(AddTask,AddTaskAdmin)