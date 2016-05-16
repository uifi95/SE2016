from statistics import mean

from django.contrib import admin


# Register your models here.
from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.pdfgen import canvas

from LoginApp.models import Student
from StudentApp.models import StudyGroup
from TeacherApp.models import StudentAssignedCourses, Grade

def return_grade(course, student):
    if Grade.objects.filter(course=course, student=student):
        return Grade.objects.get(course=course, student=student).value
    else:
        return 0

def print_all(modeladmin, request, queryset):
    print(queryset)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Times-Roman",25)
    p.drawString(50,765,"Students in groups ordered by professional results")
    xx = 700
    c = 0
    grouplist = queryset
    for group in grouplist:
        p.setFont("Times-Roman",15)
        p.drawString(102, xx, "Group: " + str(group.number))
        xx = xx - 30
        l = []
        for student in Student.objects.filter(group=group):
            courses = [i.course for i in StudentAssignedCourses.objects.filter(student=student)]
            medie = mean([return_grade(course, student) for course in courses])
            student_detail = []
            student_detail.append(student.first_name)
            student_detail.append(student.last_name)
            student_detail.append(round(medie,2))
            l.append(student_detail)
        ordonata = sorted(l, key=lambda x: x[2], reverse=True)
        for student in ordonata:
            p.setFont("Times-Roman",12)
            p.drawString(80, xx, student[0] + " " + student[1] + " " + str(student[2]))
            c = c + 1
            if c > 15:
                p.showPage()
                c = 0
                xx = 700
            xx = xx - 30
        xx = xx - 20
    # f = Paragraph("Our title", styles["Normal"])
    # p.setFont("Times-Roman",20)
    # p.drawString(102,600,str(queryset))

    p.showPage()
    p.save()
    return response
print_all.short_description = "Print all selected groups"

class GroupAdmin(admin.ModelAdmin):
    fields = ['number', 'year', 'study_line']
    list_display = ['number', 'year', 'study_line']
    actions = [print_all]
admin.site.register(StudyGroup, GroupAdmin)
