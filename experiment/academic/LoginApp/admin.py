from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'id_number', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']

# Register your models here.
admin.site.register(Student, StudentAdmin)