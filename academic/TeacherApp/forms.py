from django import forms
from django.core.exceptions import ValidationError

from LoginApp.models import Teacher
from StudentApp.models import StudyLine, Year
from django.forms import Form, CharField, ChoiceField

from TeacherApp.models import OptionalCourse


class OptionalForm(Form):
    name = CharField(max_length=100)
    study_line = ChoiceField(label="Study line", choices=StudyLine.CHOICES)
    year = ChoiceField(label="Year", choices=Year.CHOICES)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Form, self).__init__(*args, **kwargs)

    def clean(self):
        current_teacher = Teacher.objects.filter(user=self.user)
        if OptionalCourse.objects.filter(name=self.cleaned_data['name'], study_line=self.cleaned_data['study_line'],
                                         year=self.cleaned_data['year'],
                                         teacher=current_teacher).exists():
            raise ValidationError("Optional already exists.", code="opt_exst")
        if OptionalCourse.objects.filter(teacher=current_teacher).count() == 2:
            raise ValidationError("You can't add more optionals,maximum 2,delete some to add more.", code="opt_mt_two")
