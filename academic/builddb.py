import os
import random

import django


os.environ['DJANGO_SETTINGS_MODULE'] = "academic.settings"

django.setup()

from django.contrib.auth.models import User
from TeacherApp.models import Grade, Course, PackageToOptionals, StudentOptions, StudentAssignedCourses, OptionalPackage
from StudentApp.models import StudyGroup, StudyLine, Year
from django.db.utils import IntegrityError

from LoginApp.models import Client, Student, Teacher, Staff, CurrentYearState, YearState

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

if __name__ == "__main__":
    firstNames = ["Emil", "Ion", "Cornel", "Maria", "Vasile", "Bogdan", "Ana", "Laura", "Melisa", "Sergiu", "Ionut"]
    lastNames = ["Mihalache", "Tomescu", "Miclea", "Ciobanu", "Rusu", "Cosma", "Centea", "Pop", "Popa", "Rus", "Dan",
                 "Pan", "Cornea"]
    print("Cleaning up db...")
    cleanDB()
    print ("Creating year state...")
    yearState = CurrentYearState(year=2014, semester=1, crtState=YearState.OPTIONAL_PROPOSAL)
    yearState.save()
    print ("Creating groups...")
    groups = []
    for i in range(9):
        gr = StudyGroup(number=910 + i, study_line=random.choice(StudyLine.CHOICES)[1],
                            year=random.choice(Year.CHOICES)[1])
        gr.save()
        groups.append(gr)
    print("Creating 50 students...")
    studList = []
    for i in range(50):
        s = Student(first_name=random.choice(firstNames), last_name=random.choice(lastNames), email="bla@bla.com",
                    id_number=i, group=random.choice(groups))
        s.save()
        studList.append(s)

    print("Creating 10 teachers...")
    teacherList = []
    for i in range(10):
        t = Teacher(first_name=random.choice(firstNames), last_name=random.choice(lastNames), email="bla@bla.com")
        t.save()
        teacherList.append(t)

    print("Creating 2 admins")
    adminList = []
    for i in range(2):
        a = Staff(first_name="Admin", last_name="Admin", email="bla@bla.com")
        a.save()
        a.user.set_password("parolaparola")
        a.user.save()
        a.is_activated = True
        a.save()
        adminList.append(a)

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

    cnames = ["Object oriented programming", "Software Engineering", "Web programming", "Artificial Intelligence",
              "English", "Dynamic Systems", "Cryptography", "Databases"]
    courses = []
    print("Creating 200 courses")
    for i in range(200):
        name = cnames[i % len(cnames)] + " Version " + str(i)
        c = Course(name=name, teacher=random.choice(teacherList), study_line=random.choice(StudyLine.CHOICES)[1],
                   year=random.choice(Year.CHOICES)[1], semester=random.choice([1,2]), number_credits=8)
        c.save()
        courses.append(c)

    # Grades happen after preferences and assignment
    """
    print("Generating at most 50 grades")
    grades = []
    for i in range(50):
        c = random.choice(courses)
        goodStud = list(filter(lambda x: x.group.study_line == c.study_line and x.group.year == c.year, studList))
        if len(goodStud) == 0:
            continue
        s = random.choice(goodStud)
        g = Grade(value=random.choice(range(1, 11)), student=s, course=c)
        try:
            g.save()
        except IntegrityError:
            continue
        grades.append(g)
    """

    with open("dbinfo.txt", "w") as f:
        f.write("Activated users with password parolaparola:\n")
        for a in adminList:
            f.write("Admin: " + a.user.username + "\n")
        f.write("Student: " + studList[0].user.username + "\n")
        f.write("Teacher: " + teacherList[0].user.username + "\n")

        f.write("\nStudents:\n")
        for el in studList[1:]:
            f.write(el.user.username + "\t" + el.get_temp_pass()  + "\n")

        f.write("\nTeachers:\n")
        for el in teacherList[1:]:
            f.write(el.user.username + "\t" + el.get_temp_pass()  + "\n")

    print("Done..")


