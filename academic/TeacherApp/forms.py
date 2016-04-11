from django import forms

from StudentApp.models import StudyLine, Year
from django.forms import Form, CharField, ChoiceField


class OptionalForm(Form):
    name = CharField(max_length=100)
    study_line = ChoiceField(label="Study line", choices=StudyLine.CHOICES)
    year = ChoiceField(label="Year", choices=Year.CHOICES)

