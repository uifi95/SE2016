from django.contrib import admin


# Register your models here.
from StudentApp.models import StudyGroup


class GroupAdmin(admin.ModelAdmin):
    fields = ['number', 'year', 'study_line']
    list_display = ['number', 'year', 'study_line']

admin.site.register(StudyGroup, GroupAdmin)
