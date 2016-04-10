from django.contrib import admin

# Register your models here.
from TeacherApp.models import Course, Grade, OptionalCourse


class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'teacher', 'study_line', 'year']
    list_display = ['name', 'teacher', 'study_line', 'year']



class OptionalCourseAdmin(CourseAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class GradeAdmin(admin.ModelAdmin):
    fields = ['value', 'student', 'course']
    list_display = ['value', 'student', 'course']


admin.site.register(Course, CourseAdmin)
admin.site.register(OptionalCourse, OptionalCourseAdmin)
admin.site.register(Grade, GradeAdmin)

