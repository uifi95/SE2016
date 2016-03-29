from LoginApp.models import Teacher
from LoginApp.user_checks import teacher_check
from TeacherApp.models import Course
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from TeacherApp.forms import *

from LoginApp.models import Student

from TeacherApp.models import Grade


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def teacher_main(request):
    if not request.user.client_set.first().is_activated:
        return redirect("LoginApp:change_account")
    name = Teacher.objects.all().filter(user=request.user).first().last_name
    return render(request, 'TeacherApp/teacher_main.html', {"first_name": name, "has_permission": True})

@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def grades(request):
    if(request.GET.get('sel')):
        value = request.GET.get('grade')
        studentname = request.GET.get('selectedstudent')
        stlastname= studentname.split(" ")[0]
        student = Student.objects.all().filter(first_name=stlastname)
        coursename = request.GET.get('selectedcourse')
        course = Course.objects.all().filter(name=coursename)
        grade = Grade(value=value,student=student[0],course=course[0])
        grade.save()
    current_teacher = request.user.client_set.first()
    students = Student.objects.all()
    courses = Course.objects.all().filter(teacher=current_teacher)
    return render(request, "TeacherApp/grades.html", {"courses": courses,"students":students, "has_permission": True})
