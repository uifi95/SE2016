from django.contrib import admin
from .models import Student, Staff, Teacher


class StudentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'id_number', 'email', 'group']
    list_display = ['get_user', 'last_name', 'first_name', 'group', 'email', 'is_activated',
                    'get_temp_pass']


# No need for teacher admin right now
# class TeacherAdmin(admin.ModelAdmin):
#     fields = ['first_name', 'last_name', 'email']
#     list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


class StaffAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Teacher, StaffAdmin)
