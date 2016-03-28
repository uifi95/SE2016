from __future__ import unicode_literals

from django.db import models


# Create your models here.
class StudyLine(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
