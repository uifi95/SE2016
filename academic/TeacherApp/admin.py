from django.contrib import admin

# Register your models here.
from TeacherApp.models import Course, Grade, OptionalCourse, OptionalPackage


class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'teacher', 'study_line', 'year', 'number_credits']
    list_display = ['name', 'teacher', 'study_line', 'year', 'number_credits']


class OptionalCourseAdmin(CourseAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GradeAdmin(admin.ModelAdmin):
    fields = ['value', 'student', 'course']
    list_display = ['value', 'student', 'course']


class OptionalPackageAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'department']
    list_display = ['name', 'year', 'department']


admin.site.register(Course, CourseAdmin)
admin.site.register(OptionalCourse, OptionalCourseAdmin)
admin.site.register(Grade, GradeAdmin)
# Not sure admin should see optional packages, at least not in this form
admin.site.register(OptionalPackage, OptionalPackageAdmin)
