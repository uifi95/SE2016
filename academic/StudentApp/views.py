from statistics import mean

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from reportlab.pdfgen import canvas
from LoginApp.models import Student
from LoginApp.user_checks import student_check, admin_check
from StudentApp.admin import return_grade
from StudentApp.forms import SelectOptionals, SelectInterval, YearSemesterDropDown
from TeacherApp.models import Grade, PackageToOptionals, OptionalCourse, StudentOptions, \
    StudentAssignedCourses


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(student_check, login_url=reverse_lazy('LoginApp:login'))
def main_page(request):
    if not request.user.client_set.first().is_activated:
        return redirect("LoginApp:change_account")
    name = Student.objects.all().filter(user=request.user).first().last_name
    return render(request, "StudentApp/student_main.html", {"first_name": name, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(student_check, login_url=reverse_lazy('LoginApp:login'))
def grades(request):
    current_student = request.user.client_set.first()
    form = YearSemesterDropDown()
    if request.POST:
        form = YearSemesterDropDown(data=request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            semester = form.cleaned_data['semester']
            courses = [i.course for i in
                       StudentAssignedCourses.objects.filter(student=current_student, course__year=year,
                                                             course__semester=semester)]
            for i in range(len(courses)):
                if Grade.objects.filter(course=courses[i]):
                    grade = Grade.objects.get(course=courses[i]).value
                    courses[i] = (courses[i], grade)
                else:
                    courses[i] = (courses[i], "None")
    else:
        courses = [i.course for i in
                   StudentAssignedCourses.objects.filter(student=current_student, course__year=1, course__semester=1)]
        for i in range(len(courses)):
            if Grade.objects.filter(course=courses[i]):
                grade = Grade.objects.get(course=courses[i]).value
                courses[i] = (courses[i], grade)
            else:
                courses[i] = (courses[i], "None")
    return render(request, "StudentApp/grades.html", {"table": courses, "form": form, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(student_check, login_url=reverse_lazy('LoginApp:login'))
def study_contract(request):
    student = Student.objects.all().filter(user=request.user).first()
    if request.POST:
        form = SelectOptionals(student=student, year=student.group.year, data=request.POST)
        if form.is_valid():
            for course_name in form.cleaned_data:
                course = OptionalCourse.objects.filter(name=course_name).first()
                package = PackageToOptionals.objects.filter(course=course).first().package
                pref = form.cleaned_data[course_name]
                existent_options = StudentOptions.objects.filter(student=student, course=course, package=package)
                if existent_options.count() > 1:
                    opt = existent_options.first()
                    opt.preference = pref
                    opt.save()
                else:
                    ns = StudentOptions(student=student, course=course, package=package, preference=pref)
                    ns.save()
            return redirect("StudentApp:main")
        else:
            return render(request, "StudentApp/study_contracts.html", {'form': form, "has_permission": True})

    else:
        form = SelectOptionals(student, student.group.year)
        return render(request, "StudentApp/study_contracts.html", {'form': form, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(admin_check, login_url=reverse_lazy('LoginApp:login'))
def interval(request):
    if request.POST:
        form = SelectInterval(data=request.POST)
        if form.is_valid():
            leftval = int(form.cleaned_data['leftInterval'])
            rightval = int(form.cleaned_data['rightInterval'])
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="StudentsByInterval.pdf"'

            p = canvas.Canvas(response)
            p.setFont("Times-Roman", 20)
            p.drawString(70, 765, "Students ordered by professional results from each year ")
            xx = 700
            c = 0
            p.setFont("Times-Roman", 15)
            p.drawString(102, xx, "Interval: " + "(" + str(leftval) + ", " + str(rightval) + ")")
            xx -= 30
            l = []

            for student in Student.objects.all():
                courses = [i.course for i in StudentAssignedCourses.objects.filter(student=student)]
                medie = mean([return_grade(course, student) for course in courses])
                student_detail = [student.first_name, student.last_name, round(medie, 2),student.group.year,student.group.number]
                l.append(student_detail)
            year1 = [i for i in l if i[3]==1]
            year2 =[i for i in l if i[3]==2]
            year3=[i for i in l if i[3]==3]
            ordonata1 = sorted(year1, key=lambda x: x[2], reverse=True)
            ordonata2 = sorted(year2, key=lambda x: x[2], reverse=True)
            ordonata3 = sorted(year3, key=lambda x: x[2], reverse=True)
            ordonata=[ordonata1,ordonata2,ordonata3]
            p.setFont("Times-Roman", 15)

            for ord in ordonata:
                p.drawString(10, xx, "Year:" + str(ord[0][3]))
                p.drawString(80, xx, "Name ")
                p.drawString(270, xx, "Average Grade")
                p.drawString(440, xx, "Group")
                xx = xx - 30
                for student in ord:
                    if leftval < student[2] < rightval:
                        p.setFont("Times-Roman", 12)
                        p.drawString(80, xx, student[1] + " " + student[0])
                        p.drawString(300, xx, str(student[2]))
                        p.drawString(450,xx,str(student[4]))
                        c += 1
                        if c > 15:
                            p.showPage()
                            c = 0
                            xx = 700
                        xx -= 30
                xx -= 20
                xx=765
                p.showPage()
            p.save()
            return response
        else:
            return render(request, "StudentApp/interval.html", {'form': form, "has_permission": True})
    else:
        form = SelectInterval()
        return render(request, "StudentApp/interval.html", {'form': form, "has_permission": True})
