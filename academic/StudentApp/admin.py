from django.contrib import admin


# Register your models here.
from StudentApp.models import StudyLine


class StudyLineAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']

admin.site.register(StudyLine, StudyLineAdmin)
