from django.db import models

# Create your models here.
from LoginApp.models import Teacher, Student, StudyLine, CurrentYearState
from StudentApp.models import Year, StudyGroup


class Course(models.Model):
    class Meta:
        unique_together = (('name', 'teacher', 'study_line', 'year', 'academic_year'),)

    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, null=False, default=1)
    study_line = models.CharField(max_length=50, choices=StudyLine.CHOICES)
    year = models.IntegerField("Year", choices=Year.CHOICES, default=1)
    academic_year = models.IntegerField("Course academic year", default=2014)
    semester = models.IntegerField("Semester", choices=[(1, 1), (2, 2)], default=1)
    number_credits = models.IntegerField("Number of credits", default=6)

    def save(self, *args, **kwargs):
        if not self.academic_year:
            self.academic_year = CurrentYearState.objects.first().year
        super(Course, self).save(*args, **kwargs)

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
    second_date = models.BooleanField(default=False)

    def __str__(self):
        return str(self.value) + " " + str(self.course)


class OptionalPackage(models.Model):
    name = models.CharField(unique=True, max_length=30, null=False, default="CO0")
    year = models.IntegerField("Year", choices=Year.CHOICES, default=1)
    academic_year = models.IntegerField("Package academic year", default=2014)
    semester = models.IntegerField("Semester", choices=[(1, 1), (2, 2)], default=1)
    number_of_credits = models.IntegerField("Number of credits", default=4)
    department = models.CharField(max_length=50, choices=StudyLine.CHOICES, default=StudyLine.CHOICES[0])

    def save(self, *args, **kwargs):
        self.academic_year = CurrentYearState.objects.first().year
        super(OptionalPackage, self).save(*args, **kwargs)


class PackageToOptionals(models.Model):
    package = models.ForeignKey(OptionalPackage, on_delete=models.CASCADE)
    course = models.OneToOneField(OptionalCourse, on_delete=models.CASCADE)


class StudentOptions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    package = models.ForeignKey(OptionalPackage, on_delete=models.CASCADE)
    course = models.ForeignKey(OptionalCourse, on_delete=models.CASCADE)
    preference = models.IntegerField("Course preference")


class StudentAssignedCourses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField("Academic year")


class ExaminationPeriod(models.Model):
    exam_date = models.DateField("Examination Date")
    reexam_date = models.DateField("Reexamination Date")
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.group) + " " + str(self.course)
