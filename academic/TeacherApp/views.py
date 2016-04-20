from django.core.exceptions import ValidationError
from django.db import IntegrityError

from LoginApp.models import Teacher, StudyLine, ChiefOfDepartment
from LoginApp.user_checks import teacher_check, dchief_check
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from StudentApp.models import Year
from TeacherApp.forms import *

from LoginApp.models import Student

from TeacherApp.models import Grade, OptionalCourse, Course


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def teacher_main(request):
    if not request.user.client_set.first().is_activated:
        return redirect("LoginApp:change_account")
    name = Teacher.objects.all().filter(user=request.user).first().last_name
    return render(request, 'TeacherApp/teacher_main.html', {"first_name": name, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(dchief_check, login_url=reverse_lazy('LoginApp:login'))
def dchief_page(request):
    opt = OptionalCourse.objects.filter(
        study_line=ChiefOfDepartment.objects.filter(user=request.user).first().department).order_by("teacher")
    return render(request, 'TeacherApp/dchief.html', {"optionals": opt, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def optionals(request):
    current_teacher = request.user.client_set.first()
    optional_list = OptionalCourse.objects.filter(teacher=current_teacher)
    return render(request, "TeacherApp/optionals.html", {"optionals": optional_list, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def delete_optional(request, optional_id):
    course = OptionalCourse.objects.filter(id=optional_id)
    course.delete()
    return redirect("TeacherApp:optionals")


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def add_optional(request):
    current_teacher = request.user.client_set.first().teacher
    if request.POST:
        optform = OptionalForm(user=request.user, data=request.POST)
        if optform.is_valid():
            name = optform.cleaned_data["name"]
            studyLine = optform.cleaned_data["study_line"]
            year = optform.cleaned_data["year"]
            newOpt = OptionalCourse(name=name, study_line=studyLine, year=year, teacher=current_teacher)
            newOpt.save()
            return redirect("TeacherApp:optionals")
        else:
            return render(request, "TeacherApp/add_optional.html", {'form': optform})
    else:
        newForm = OptionalForm(user=request.user)
        return render(request, "TeacherApp/add_optional.html", {'form': newForm})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def courses(request):
    current_teacher = request.user.client_set.first()
    all_courses = Course.objects.filter(teacher=current_teacher)
    study_lines = [i[0] for i in StudyLine.CHOICES if all_courses.filter(study_line=i[0]).count() != 0]
    years = []
    for st in study_lines:
        years = years + [[i[0] for i in Year.CHOICES if all_courses.filter(year=i[0], study_line=st).count() != 0]]
    return render(request, "TeacherApp/courses.html",
                  {"courses": all_courses, "study_lines": zip(study_lines, years), "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def students(request, course_id):
    course = get_object_or_404(Course, pk=int(course_id))
    args = ('group', 'first_name', 'last_name')
    all_students = Student.objects.filter(group__study_line=course.study_line, group__year=course.year).order_by(*args)
    args = ('student__' + i for i in args)
    grades = [elem.value for elem in
              Grade.objects.filter(student__in=all_students, course=course).order_by(*args)]
    count = 0
    for student in all_students:
        if not Grade.objects.filter(student=student, course=course).exists():
            grades = grades[:count] + [''] + grades[count:]
        count += 1
    return render(request, "TeacherApp/students.html",
                  {"students": zip(all_students, grades), 'course_id': course_id, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def edit(request, course_id, student_id, grade_exists=None):
    form = GradeForm()
    course = get_object_or_404(Course, pk=int(course_id))
    args = ('group', 'first_name', 'last_name')
    all_students = Student.objects.filter(group__study_line=course.study_line, group__year=course.year).order_by(*args)
    args = ('student__' + i for i in args)
    grades = [elem.value for elem in
              Grade.objects.filter(student__in=all_students, course=course).order_by(*args)]
    count = 0
    for student in all_students:
        if not Grade.objects.filter(student=student, course=course).exists():
            grades = grades[:count] + [''] + grades[count:]
        count += 1
    if request.POST:
        form = GradeForm(data=request.POST)
        if form.is_valid():
            value = int(form.cleaned_data['grade'])
            student = get_object_or_404(Student, pk=int(student_id))
            course = get_object_or_404(Course, pk=int(course_id))
            grade_exists = Grade.objects.filter(student=student, course=course).exists()
            if not grade_exists:
                grade = Grade(value=value, student=student, course=course)
            else:
                grade = Grade.objects.filter(student=student, course=course).first()
                grade.value = value
            grade.save()
            return students(request, course_id)
        else:
            return render(request, "TeacherApp/edit.html",
                          {"students": zip(all_students, grades), 'form': form, "student_id": int(student_id),
                           "course_id": course_id,
                           "has_permission": True})
    return render(request, "TeacherApp/edit.html",
                  {"students": zip(all_students, grades), 'form': form, "student_id": int(student_id),
                   "course_id": course_id,
                   "has_permission": True})
