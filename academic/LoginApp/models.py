from __future__ import unicode_literals
import string
import struct
from os import urandom
from random import shuffle

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

# Create your models here.
from StudentApp.models import StudyGroup, StudyLine, Year


class Client(models.Model):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    email = models.EmailField()
    user = models.ForeignKey(User, null=True)
    temp_pass = models.CharField(max_length=40)
    is_activated = models.BooleanField("Active", default=False)
    type = models.CharField(max_length=30)

    def _gen_user(self):
        u_name = (self.first_name[0] + self.last_name).lower()
        base = u_name
        count = 0
        while User.objects.filter(username=u_name).all().count():
            u_name = base + str(count)
            count += 1
        return u_name

    def _set_type(self, type):
        group, created = Group.objects.get_or_create(name=type)
        self.user.groups.add(group)
        self.type = type

    def reset_password(self):
        self.temp_pass = self._gen_pass()
        self.save()
        self.is_activated = False
        self.save()
        self.user.set_password(self.temp_pass)
        self.user.save()

    @staticmethod
    def _gen_pass():
        alphabet = list(string.ascii_letters + string.digits + "!@#$%^&*")
        shuffle(alphabet)
        rbytes = urandom(13)
        password = ""
        for el in rbytes:
            bval = struct.unpack('B', bytes([el]))[0]
            password += alphabet[bval % len(alphabet)]
        return password

    def _create_user(self):
        self.temp_pass = self._gen_pass()
        self.user = User.objects.create_user(username=self._gen_user(), password=self.temp_pass, email=self.email)

    def get_temp_pass(self):
        if self.is_activated:
            return ""
        else:
            return self.temp_pass

    def get_user(self):
        return self.user.get_username()

    get_user.short_description = "Username"
    get_temp_pass.short_description = "Temporary password"

    def __str__(self):
        return self.last_name + " " + self.first_name


class Staff(Client):
    class Meta:
        verbose_name_plural = 'Staff'

    def save(self, *args, **kwargs):
        if not self.pk:
            self._create_user()
            self._set_type("staff")
            self.user.is_staff = True
            self.user.save()
            self.user.is_admin = True
            self.user.save()
            self.user.is_superuser = True
            self.user.save()
        super(Staff, self).save(*args, **kwargs)


class Student(Client):
    id_number = models.IntegerField("Identification number", unique=True)
    group = models.ForeignKey(StudyGroup, null=False, default=1)
    is_enrolled = models.BooleanField("Currently enrolled", default=True)

    def _gen_user(self):
        if len(self.last_name) >= 2:
            firstTwo = self.last_name[:2]
        else:
            firstTwo = self.last_name
        if len(self.first_name) >= 2:
            lastTwo = self.first_name[:2]
        else:
            lastTwo = self.first_name
        return (firstTwo + lastTwo + str(self.id_number)).lower()

    def save(self, *args, **kwargs):
        if not self.pk:
            self._create_user()
            self._set_type("student")
        super(Student, self).save(*args, **kwargs)


class Teacher(Client):
    def save(self, *args, **kwargs):
        if not self.pk:
            self._create_user()
            self._set_type("teacher")
            self.user.is_admin = True
            self.user.save()
        super(Teacher, self).save(*args, **kwargs)


class ChiefOfDepartment(Teacher):
    department = models.CharField(max_length=50, choices=StudyLine.CHOICES, unique=True, null=True)

    def save(self, *args, **kwargs):
        super(ChiefOfDepartment, self).save(*args, **kwargs)
        self._set_type("dchief")
        self.user.save()


class YearState:
    SEMESTER_1 = "First Semester going on"
    SEMESTER_2 = "Second semester going on"
    SIGN_CONTRACTS = "Contract signing going on"
    OPTIONAL_PROPOSAL = "Proposing optionals going on"
    OPTIONAL_PACKAGES = "Optional package building going on"
    CHOICHES = [(SEMESTER_1, SEMESTER_1),
                (SEMESTER_2, SEMESTER_2),
                (OPTIONAL_PROPOSAL, OPTIONAL_PROPOSAL),
                (OPTIONAL_PACKAGES, OPTIONAL_PACKAGES),
                (SIGN_CONTRACTS, SIGN_CONTRACTS)]


class CurrentYearState(models.Model):
    year = models.IntegerField("Current Year")
    semester = models.IntegerField("Current Semester")
    crtState = models.CharField("Current State", max_length=50, choices=YearState.CHOICHES)
    oldState = models.CharField("Old State", max_length=50, choices=YearState.CHOICHES, null=True)

    class Meta:
        verbose_name_plural = 'Current year state'

    def execute_transition(self):
        # Check credit counts work
        from TeacherApp.models import OptionalCourse, Course, OptionalPackage
        from TeacherApp.models import StudentAssignedCourses, StudentOptions
        from TeacherApp.models import Grade

        if self.oldState == YearState.OPTIONAL_PACKAGES:
            for year in Year.CHOICES:
                for semester in [1, 2]:
                    for study_line in StudyLine.CHOICES:
                        checkYear = year[0]
                        creditCount = 0
                        courses = Course.objects.filter(academic_year=self.year, year=checkYear, semester=semester,
                                                        study_line=study_line[0])
                        for c in courses:
                            if isinstance(c, OptionalCourse):
                                continue
                            creditCount += c.number_credits
                        optionals = OptionalPackage.objects.filter(academic_year=self.year, year=checkYear,
                                                                   semester=semester)
                        for opt in optionals:
                            creditCount += opt.number_of_credits
                        if creditCount < 30:
                            raise ValidationError("Maximum credit count is too small (is " + str(creditCount) + \
                                                  " minimum is 30) for year: " + str(checkYear) + " semester: " + \
                                                  str(semester) + " study line: " + study_line[0])

        if self.oldState == YearState.SIGN_CONTRACTS:
            # Now start assigning courses to students
            students = Student.objects.filter(is_enrolled=True)
            for st in students:
                for semester in [1, 2]:
                    # first assign mandatory courses for the year
                    courses = Course.objects.filter(academic_year=self.year, year=st.group.year, semester=semester,
                                                    study_line=st.group.study_line)
                    for c in courses:
                        if isinstance(c, OptionalCourse):
                            continue
                        nas = StudentAssignedCourses(student=st, course=c, year=self.year)
                        nas.save()

                    # now assign courses not passed in previous years
                    stcourses = StudentAssignedCourses.objects.filter(student=st, course__semester=semester).exclude(
                        course__year=st.group.year)
                    for c in stcourses:
                        grade = Grade.objects.filter(student=st, course=c)
                        if grade.count() == 0 or grade.first().value() < 5:
                            newCourse = Course.objects.filter(academic_year=self.year, semester=semester, name=c.name,
                                                              study_line=st.group.study_line)
                            if newCourse.count() > 0:
                                nas = StudentAssignedCourses(student=st, course=newCourse.first(), year=self.year)
                                nas.save()
                            else:
                                # If no new matching course exist, assign old one and hope for the best
                                nas = StudentAssignedCourses(student=st, course=c, year=self.year)
                                nas.save()

            # now start optional course assignment
            numberOfPreferences = {}
            for st in students:
                preferences = StudentOptions.objects.filter(student=st, package__academic_year=self.year)
                for p in preferences:
                    if p.preference == 1:
                        numberOfPreferences[p.course] += 1
            packages = OptionalPackage.objects.filter(academic_year=self.year)
            for st in students:
                for p in packages:
                    is_good = False
                    prefs = StudentOptions.objects.filter(student=st, package=p)
                    for pr in prefs:
                        if pr.preference == 1 and numberOfPreferences[pr.course] >= 20:
                            # all good here
                            nas = StudentAssignedCourses(student=st, course=pr.course, year=self.year)
                            nas.save()
                            is_good = True
                            break
                    if not is_good:
                        sp = sorted(prefs, key=lambda x: x.preference)
                        for pref in sp:
                            if numberOfPreferences[pref.course] >= 20:
                                nas = StudentAssignedCourses(student=st, course=pref.course, year=self.year)
                                nas.save()
                                is_good = True
                                break
                    # Maybe he didn't enter any options
                    if not is_good:
                        # assign to first course with enough people if any
                        for el in numberOfPreferences.keys():
                            if numberOfPreferences[el] >= 20:
                                nas = StudentAssignedCourses(student=st, course=el, year=self.year)
                                nas.save()
                                is_good = True
                                break

                    # if still not good, assign to first course in the package
                    if not is_good:
                        from TeacherApp.models import PackageToOptionals
                        course = PackageToOptionals.objects.filter(package=p).first().course
                        nas = StudentAssignedCourses(student=st, course=course, year=self.year)
                        nas.save()

        if self.oldState == YearState.SEMESTER_2:
            # promote appropriate students
            students = Student.objects.filter(is_enrolled=True)
            for st in students:
                creditCount = 0
                asn = StudentAssignedCourses.objects.filter(student=st, year=self.year)
                for el in asn:
                    grade = Grade.objects.filter(course=el.course, student=st)
                    if grade.count() == 0:
                        continue
                    grade = grade.first().value
                    if grade >= 5:
                        creditCount += el.course.number_credits

                if creditCount > 30:
                    if st.group.year == Year.CHOICES[-1][0]:
                        # student graduates
                        st.is_enrolled = False
                        st.save()
                        continue
                    # promote student
                    ng = StudyGroup.objects.filter(number=st.group.number + 10)
                    if ng.count() == 0:
                        ng = StudyGroup(number=st.group.number + 10, year=st.group.year + 1,
                                        study_line=st.group.study_line)
                        ng.save()
                    else:
                        ng = ng.first()
                    st.group = ng
                    st.save()
            self.year += 1
            self.semester = 1
            # generate next year courses
            courses = Course.objects.filter(year=self.year - 1)
            for c in courses:
                if isinstance(c, OptionalCourse):
                    continue
                nc = Course(name=c.name, teacher=c.teacher, study_line=c.study_line, year=c.year, semester=c.semester,
                            academic_year=self.year,
                            number_credits=c.number_credits)
                nc.save()

        if self.oldState == YearState.SEMESTER_1:
            self.semester += 1

    def clean(self, *args, **kwargs):
        if self.oldState is not None:
            crtIdx = YearState.CHOICHES.index((self.crtState, self.crtState))
            if YearState.CHOICHES[crtIdx - 1][0] != self.oldState:
                raise ValidationError("Invalid state transition!")
        self.execute_transition()
        super(CurrentYearState, self).clean()

    def full_clean(self, *args, **kwargs):
        return self.clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.oldState = self.crtState

        super(CurrentYearState, self).save(*args, **kwargs)


# SIGNALS start here
# Global flag to avoid infinite recursion
is_in_pre_delete = False


@receiver(pre_delete, sender=Client)
def pre_delete_client(sender, **kwargs):
    global is_in_pre_delete
    if is_in_pre_delete:
        return
    if not isinstance(kwargs["instance"], Client):
        return
    is_in_pre_delete = True
    user = kwargs["instance"].user
    kwargs["instance"].user = None
    user.delete()
    is_in_pre_delete = False
