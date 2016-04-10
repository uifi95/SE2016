from django.db import models

# Create your models here.
from LoginApp.models import Teacher, Student, StudyLine


class Course(models.Model):
    class Meta:
        unique_together = (('name', 'teacher', 'study_line'),)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, null=False, default=1)
    study_line = models.CharField(max_length=50, choices=StudyLine.CHOICES)

    def __str__(self):
        return self.name


class Grade(models.Model):
    class Meta:
        unique_together = (('student', 'course'),)

    value = models.IntegerField(unique=False, default=0, null=True)
    student = models.ForeignKey(Student, null=False)
    course = models.ForeignKey(Course, null=False)

    def __str__(self):
        return str(self.value) + " " + str(self.course)
