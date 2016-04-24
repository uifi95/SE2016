from django.db import models

# Create your models here.
from LoginApp.models import Teacher, Student, StudyLine
from StudentApp.models import Year


class Course(models.Model):
    class Meta:
        unique_together = (('name', 'teacher', 'study_line', 'year'),)

    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, null=False, default=1)
    study_line = models.CharField(max_length=50, choices=StudyLine.CHOICES)
    year = models.IntegerField("Year", choices=Year.CHOICES, default=1)
    number_credits = models.IntegerField("Number of credits", default=6)

    def __str__(self):
        return self.name


class OptionalCourse(Course):
    pass


class Grade(models.Model):
    class Meta:
        unique_together = (('student', 'course'),)

    value = models.IntegerField(unique=False, default=0, null=True)
    student = models.ForeignKey(Student, null=False)
    course = models.ForeignKey(Course, null=False)

    def __str__(self):
        return str(self.value) + " " + str(self.course)

class OptionalPackage(models.Model):
    name = models.CharField(max_length=30, null=True)
    year = models.IntegerField("Year", choices=Year.CHOICES, default=1)
    department = models.CharField(max_length=50, choices=StudyLine.CHOICES, default=StudyLine.CHOICES[0])


class PackageToOptionals(models.Model):
    package = models.ForeignKey(OptionalPackage, on_delete=models.CASCADE)
    course = models.OneToOneField(OptionalCourse, on_delete=models.CASCADE)
