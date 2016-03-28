from django.contrib import admin

# Register your models here.
from TeacherApp.models import Course, Grade


class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'teacher', 'study_line']
    list_display = ['name', 'teacher', 'study_line']


class GradeAdmin(admin.ModelAdmin):
    fields = ['value', 'student', 'course']
    list_display = ['value', 'student', 'course']


admin.site.register(Course, CourseAdmin)
admin.site.register(Grade, GradeAdmin)
