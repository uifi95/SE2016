from django import forms
from TeacherApp.models import Course
from django.forms import Form


class selectcoursesform(Form):
        courses = forms.ChoiceField(Course.objects.all())
