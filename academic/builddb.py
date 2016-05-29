import os
import random
from django.db import transaction
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "academic.settings"

django.setup()

from django.contrib.auth.models import User, Group
from TeacherApp.models import Grade, Course, PackageToOptionals, StudentOptions, StudentAssignedCourses, OptionalPackage
from StudentApp.models import StudyGroup, StudyLine, Year
from django.db.utils import IntegrityError

from LoginApp.models import Client, Student, Teacher, Staff, CurrentYearState, YearState, ChiefOfDepartment


def delete_all(bla):
    pass


def cleanDB():
    delete_all(CurrentYearState.objects.all().delete())
    delete_all(OptionalPackage.objects.all().delete())
    delete_all(PackageToOptionals.objects.all().delete())
    delete_all(StudentOptions.objects.all().delete())
    delete_all(StudentAssignedCourses.objects.all().delete())
    delete_all(Client.objects.all().delete())
    delete_all(Grade.objects.all().delete())
    delete_all(StudyGroup.objects.all().delete())
    delete_all(Course.objects.all().delete())
    delete_all(Student.objects.all().delete())
    delete_all(Teacher.objects.all().delete())
    delete_all(Staff.objects.all().delete())
    delete_all(User.objects.all().delete())

@transaction.atomic
def create_teachers(count):
    teacherList = []
    for i in range(count):
        t = Teacher(first_name=random.choice(firstNames), last_name=random.choice(lastNames), email="bla@bla.com")
        t.save()
        teacherList.append(t)
    return teacherList

@transaction.atomic
def create_admins(count):
    adminList = []
    for i in range(count):
        a = Staff(first_name="Admin", last_name="Admin", email="bla@bla.com")
        a.save()
        a.user.set_password("parolaparola")
        a.user.save()
        a.is_activated = True
        a.save()
        adminList.append(a)
    return adminList

@transaction.atomic
def create_groups(count):
    groups = []
    sli = 6
    for sl in StudyLine.CHOICES:
        sli += 1
        yri = 1
        for yr in Year.CHOICES:
            for i in range(count):
                nb = sli * 100 + yri * 10 + i
                gr = StudyGroup(number=nb, study_line=sl[1], year=yr[1])
                gr.save()
                groups.append(gr)
            yri += 1
    return groups

@transaction.atomic
def create_students(count, groups):
    studList = []
    idn = 0
    for sl in StudyLine.CHOICES:
        for yr in Year.CHOICES:
            goodGroups = list(filter(lambda x: x.year == yr[1] and x.study_line == sl[1], groups))
            for i in range(count):
                idn += 1
                s = Student(id_number=idn, first_name=random.choice(firstNames), last_name=random.choice(lastNames), email="bla@bla.com", group=random.choice(goodGroups))
                s.save()
                studList.append(s)
    return studList

@transaction.atomic
def create_students_year(count, groups, year, stidx):
    studList = []
    idn = stidx
    for sl in StudyLine.CHOICES:
        goodGroups = list(filter(lambda x: x.year == year and x.study_line == sl[1], groups))
        for i in range(count):
            idn += 1
            s = Student(id_number=idn, first_name=random.choice(firstNames), last_name=random.choice(lastNames), email="bla@bla.com", group=random.choice(goodGroups))
            s.save()
            studList.append(s)
    return studList

@transaction.atomic
def create_dchiefs():
    dcfs = []
    for sl in StudyLine.CHOICES:
        dc = ChiefOfDepartment(department=sl[1], first_name=random.choice(firstNames),
                           last_name=random.choice(lastNames), email="bla@bla.com")
        dc.save()
        dc.user.set_password("parolaparola")
        dc.user.save()
        dc.is_activated = True
        dc.save()
        dcfs.append(dc)
    return dcfs

@transaction.atomic
def create_courses():
    courses = []
    idx = 0
    for sl in StudyLine.CHOICES:
        for yr in Year.CHOICES:
            for s in range(1, 3):
                for i in range(5):
                    name = random.choice(cnames) + " Version " + str(idx)
                    c = Course(name=name, teacher=random.choice(teacherList), study_line=sl[1],
                               year=yr[1], semester=s, number_credits=6)
                    c.save()
                    courses.append(c)
                    idx += 1
    return courses
@transaction.atomic
def generate_grades(yearState):
    asgn = StudentAssignedCourses.objects.filter(year=yearState.year)
    for a in asgn:
        if a.course.semester == yearState.semester:
            grade = Grade(value=random.randint(2,10), student=a.student, course=a.course)
            grade.save()

if __name__ == "__main__":
    firstNames = ["Emil", "Ion", "Cornel", "Maria", "Vasile", "Bogdan", "Ana", "Laura", "Melisa", "Sergiu", "Ionut"]
    lastNames = ["Mihalache", "Tomescu", "Miclea", "Ciobanu", "Rusu", "Cosma", "Centea", "Pop", "Popa", "Rus", "Dan",
                 "Pan", "Cornea"]
    cnames = ["Object oriented programming", "Software Engineering", "Web programming", "Artificial Intelligence",
              "English", "Dynamic Systems", "Cryptography", "Databases"]

    print("Cleaning up db...")
    cleanDB()
    print("Creating year state...")
    yearState = CurrentYearState(year=2014, semester=1, crtState=YearState.OPTIONAL_PROPOSAL)
    yearState.save()
    print("Creating 20 teachers...")
    teacherList = create_teachers(20)
    print("Creating department chiefs..")
    dch = create_dchiefs()
    teacherList += dch
    print("Creating 2 admins")
    adminList = create_admins(2)
    print("Creating 4 groups for each studyline/year combination")
    groups = create_groups(4)
    print("Creating 50 students for each year/studyline")
    studList = create_students(50, groups)
    print("Creating courses for each studyline/year")
    courses = create_courses()
    print("Moving to start of first semester and generating grades...")
    yearState.crtState = YearState.OPTIONAL_PACKAGES
    yearState.save()
    yearState.crtState = YearState.SIGN_CONTRACTS
    yearState.save()
    yearState.crtState = YearState.SEMESTER_1
    yearState.save()
    generate_grades(yearState)
    print("Moving to start of second semester and generating grades...")
    yearState.crtState = YearState.SEMESTER_2
    yearState.save()
    generate_grades(yearState)
    print("Finishing year and adding 50 incoming students per studyline for first year")
    yearState.crtState = YearState.OPTIONAL_PROPOSAL
    yearState.save()
    nst = create_students_year(50, groups, Year.CHOICES[0][1], len(studList))
    studList += nst
    print("Generating grades for this year, moving to next semester")
    yearState.crtState = YearState.OPTIONAL_PACKAGES
    yearState.save()
    yearState.crtState = YearState.SIGN_CONTRACTS
    yearState.save()
    yearState.crtState = YearState.SEMESTER_1
    yearState.save()
    generate_grades(yearState)
    yearState.crtState = YearState.SEMESTER_2
    yearState.save()
    generate_grades(yearState)

    s = studList[0]
    s.user.set_password("parolaparola")
    s.is_activated = True
    s.save()
    s.user.save()

    t = teacherList[0]
    t.user.set_password("parolaparola")
    t.user.save()
    t.is_activated = True
    t.save()


    with open("dbinfo.txt", "w") as f:
        f.write("Activated users with password parolaparola:\n")
        for a in adminList:
            f.write("Admin: " + a.user.username + "\n")
        f.write("Student: " + studList[0].user.username + "\n")
        f.write("Teacher: " + teacherList[0].user.username + "\n")
        for dc in dch:
            f.write("Department chief: " + dc.user.username + " study line: " + dc.department + "\n")

        f.write("\nTeachers:\n")
        for el in teacherList[1:]:
            f.write(el.user.username + "\t" + el.get_temp_pass() + "\n")

        f.write("\nStudents:\n")
        allStuds = Student.objects.all()
        for el in allStuds:
            f.write(el.user.username + "\t" + el.get_temp_pass() + " Group: " + str(el.group.number) + " Active: " + \
                    str(el.is_enrolled) + "\n")


    print("Done..")
