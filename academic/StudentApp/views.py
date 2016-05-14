from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect

# Create your views here.

from LoginApp.models import Student
from LoginApp.user_checks import student_check
from StudentApp.forms import SelectOptionals
from TeacherApp.models import Grade, PackageToOptionals, OptionalPackage, OptionalCourse, StudentOptions


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
    queryset = Grade.objects.all().filter(student=current_student).order_by("course")
    return render(request, "StudentApp/grades.html", {"table": queryset, "has_permission": True})

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
                existentOptions = StudentOptions.objects.filter(student=student, course=course, package=package)
                if existentOptions.count() > 1:
                    opt = existentOptions.first()
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