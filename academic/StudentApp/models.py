from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Year:
    CHOICES = []
    for i in range(1, 4):
        CHOICES.append((i, i))


class StudyLine:
    INFO = 'Informatics'
    MATE = 'Mathematics'
    MATE_INFO = 'Mathematics & Informatics'
    CHOICES = [(INFO, INFO),
               (MATE, MATE),
               (MATE_INFO, MATE_INFO)]


class StudyGroup(models.Model):
    number = models.IntegerField("Group Number", unique=True);
    year = models.IntegerField("Year", choices=Year.CHOICES)
    study_line = models.CharField(max_length=50, choices=StudyLine.CHOICES)

    def __str__(self):
        return "Group " + str(self.number);
