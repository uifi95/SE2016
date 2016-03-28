from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template import RequestContext

from LoginApp.models import Student
from LoginApp.user_checks import student_check
from TeacherApp.models import Grade


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
    current_student = Student.objects.all().filter(user=request.user)
    queryset = Grade.objects.all().filter(student=current_student)
    return render(request, "StudentApp/grades.html", {"table": queryset, "has_permission": True})
