from django.contrib import admin
from .models import Student, Staff, Teacher, ChiefOfDepartment, CurrentYearState


class StudentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'id_number', 'email', 'group', 'is_enrolled']
    list_display = ['is_enrolled', 'get_user', 'last_name', 'first_name', 'group', 'email', 'is_activated',
                    'get_temp_pass']


# No need for teacher admin right now
# class TeacherAdmin(admin.ModelAdmin):
#     fields = ['first_name', 'last_name', 'email']
#     list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


class StaffAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


class ChiefAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'department']
    list_display = ['get_user', 'last_name', 'first_name', 'department', 'email', 'is_activated', 'get_temp_pass']

class CrtStateAdmin(admin.ModelAdmin):
    fields = ['crtState']
    list_display = ['crtState', 'year', 'semester']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Teacher, StaffAdmin)
admin.site.register(ChiefOfDepartment, ChiefAdmin)
admin.site.register(CurrentYearState, CrtStateAdmin)