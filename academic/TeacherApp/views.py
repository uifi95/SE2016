from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from LoginApp.models import ChiefOfDepartment, CurrentYearState
from LoginApp.models import Student
from LoginApp.user_checks import teacher_check, dchief_check
from TeacherApp.forms import *
from TeacherApp.models import Grade, OptionalCourse, Course, OptionalPackage, PackageToOptionals, StudentAssignedCourses


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
    goodOptionals = []
    for el in opt:
        if PackageToOptionals.objects.filter(course=el).count() == 0:
            goodOptionals.append(el)
    goodOptionals.sort(key=lambda x: x.teacher.first_name)
    return render(request, 'TeacherApp/dchief.html', {"optionals": goodOptionals, "has_permission": True})


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
@user_passes_test(dchief_check, login_url=reverse_lazy('LoginApp:login'))
def create_package(request):
    department = request.user.client_set.first().teacher.chiefofdepartment.department
    if request.POST:
        form = PackageForm(department=department, data=request.POST)
        if form.is_valid():
            picked = form.cleaned_data['courses']
            opts = []
            for el in picked:
                opts.append(OptionalCourse.objects.filter(name=el).first())
            np = OptionalPackage(name=form.cleaned_data["name"], year=opts[0].year, department=department)
            np.save()
            for el in opts:
                po = PackageToOptionals(package=np, course=el)
                po.save()
                el.number_credits = po.number_of_credits
                el.save()
            return redirect("TeacherApp:dchief_page")
        else:
            return render(request, "TeacherApp/create_package.html", {'form': form})

    else:
        newForm = PackageForm(department)
        return render(request, "TeacherApp/create_package.html", {'form': newForm})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(dchief_check, login_url=reverse_lazy('LoginApp:login'))
def view_packages(request):
    department = request.user.client_set.first().teacher.chiefofdepartment.department
    packages = OptionalPackage.objects.filter(department=department)
    courses = []
    for package in packages:
        courses.append(OptionalCourse.objects.filter(packagetooptionals__package=package))
    return render(request, "TeacherApp/view_packages.html",
                  {"packages": zip(packages, courses),
                   "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(teacher_check, login_url=reverse_lazy('LoginApp:login'))
def delete_package(request, package_id):
    package = OptionalPackage.objects.filter(id=package_id)
    package.delete()
    return redirect("TeacherApp:view_packages")


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
            semester = optform.cleaned_data["semester"]
            newOpt = OptionalCourse(name=name, study_line=studyLine, year=year, teacher=current_teacher, semester=semester)
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
    all_students = StudentAssignedCourses.objects.filter(course=course)
    all_students = Student.objects.filter(id_number__in=all_students.values('student__id_number')).order_by(*args)
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
    all_students = StudentAssignedCourses.objects.filter(course=course)
    all_students = Student.objects.filter(id_number__in=all_students.values('student__id_number')).order_by(*args)

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


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(dchief_check, login_url=reverse_lazy('LoginApp:login'))
def view_all_courses(request):
    department = request.user.client_set.first().teacher.chiefofdepartment.department
    crtYear = CurrentYearState.objects.first().year
    crtSemester = CurrentYearState.objects.first().semester
    teachers = [("Any", "All Teachers")] + [(i.user_id, i) for i in
                                            Teacher.objects.distinct().filter(course__study_line=department, course__academic_year= crtYear,
                                                                              course__semester= crtSemester)]
    if request.POST:
        form = TeacherDropDownForm(options=teachers, data=request.POST)
        if form.is_valid():
            if form.cleaned_data["teacher"] != "Any":
                course_list = Course.objects.filter(study_line=department,
                                                    teacher=Teacher.objects.filter(
                                                    user_id=form.cleaned_data["teacher"]).first(),
                                                    year=crtYear,
                                                    semester=crtSemester)
                return render(request, "TeacherApp/view_courses.html",
                              {"courses": course_list, 'form': form, "has_permission": True})
            else:
                form = TeacherDropDownForm(options=teachers)
                course_list = Course.objects.filter(study_line=department, year=crtYear, semester=crtSemester).order_by("teacher")
                return render(request, "TeacherApp/view_courses.html",
                              {"courses": course_list, 'form': form, "has_permission": True})

    else:
        form = TeacherDropDownForm(options=teachers)

        course_list = Course.objects.filter(study_line=department, year=crtYear, semester=crtSemester).order_by("teacher")
        return render(request, "TeacherApp/view_courses.html",
                      {"courses": course_list, 'form': form, "has_permission": True})
