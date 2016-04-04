from LoginApp.models import Teacher
from LoginApp.user_checks import teacher_check
from StudentApp.models import StudyLine
from TeacherApp.models import Course
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
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
def courses(request):
    # if request.GET.get('select_button'):
    #     value = int(request.GET.get('grade'))
    #     student_name = request.GET.get('selected_student')
    #     first_name = student_name.split(" ")[0]
    #     student = Student.objects.all().filter(first_name=first_name)
    #     course_name = request.GET.get('selected_course')
    #     course = Course.objects.all().filter(name=course_name).first()
    #     grade = Grade(value=value, student=student[0], course=course[0])
    #     grade.save()
    # current_teacher = request.user.client_set.first()
    # courses = Course.objects.filter(teacher=current_teacher)
    # students = Student.objects.all()
    current_teacher = request.user.client_set.first()
    all_courses = Course.objects.filter(teacher=current_teacher)
    study_lines = StudyLine.objects.filter(course__teacher=current_teacher).distinct()
    return render(request, "TeacherApp/courses.html",
                  {"courses": all_courses, "study_lines": study_lines, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def students(request, course_id):
    course = get_object_or_404(Course, pk=int(course_id))
    args = ('first_name', 'last_name')
    all_students = Student.objects.filter(study_line=course.study_line).order_by(*args)
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
    if request.GET.get('edit_button'):
        try:
            value = int(request.GET.get('grade'))
        except Exception:
            return students(request, course_id)
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
    course = get_object_or_404(Course, pk=int(course_id))
    args = ('first_name', 'last_name')
    all_students = Student.objects.filter(study_line=course.study_line).order_by(*args)
    args = ('student__' + i for i in args)
    grades = [elem.value for elem in
              Grade.objects.filter(student__in=all_students, course=course).order_by(*args)]
    count = 0
    for student in all_students:
        if not Grade.objects.filter(student=student, course=course).exists():
            grades = grades[:count] + [''] + grades[count:]
        count += 1
    return render(request, "TeacherApp/edit.html",
                  {"students": zip(all_students, grades), "student_id": int(student_id), "course_id": course_id,
                   "has_permission": True})
