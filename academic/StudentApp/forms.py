from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, TextInput

from TeacherApp.models import OptionalPackage, PackageToOptionals, StudentOptions


def build_choice_range(max_val):
    res = []
    for i in range(1, max_val + 1):
        res.append((str(i), i))
    return res


class SelectOptionals(Form):
    def __init__(self, student, year, *args, **kwargs):
        packages = PackageToOptionals.objects.all().filter(package__year=year)
        super(Form, self).__init__(*args, **kwargs)
        for el in packages:
            selectedOptions = StudentOptions.objects.filter(student=student, course=el.course)
            if selectedOptions.count() > 0:
                self.initial[el.course.name] = selectedOptions.first().preference
            prefchoice = build_choice_range(len(packages.filter(package__name=el.package.name)))
            self.fields[el.course.name] = forms.ChoiceField(choices=prefchoice,
                                                            label=el.package.name + " - " + el.course.name,
                                                            label_suffix="")

    def clean(self):
        pref = {}
        for name in self.cleaned_data.keys():
            opt = PackageToOptionals.objects.all().filter(course__name=name).first()
            pr = self.cleaned_data[name]
            if opt.package in pref and pr in pref[opt.package]:
                if opt.package in pref and pr in pref[opt.package]:
                    raise ValidationError("Courses from one package should have different preferences!",
                                          code="bad_pref")
            if opt.package in pref:
                pref[opt.package].append(pr)
            else:
                pref[opt.package] = [pr]
        super(Form, self).clean()


class SelectInterval(Form):
    leftInterval = CharField(label="Left Interval: ", max_length=30)
    rightInterval = CharField(label="Right interval: ", max_length=30)

    def clean(self):
        try:
            if int(self.cleaned_data["leftInterval"]) not in range(0, 10) or int(self.cleaned_data["rightInterval"]) not in range(0, 10):
                raise ValidationError("Grade must be between 0 and 10", code="gr_val")
        except (ValueError, KeyError):
            raise ValidationError("Grade has to be a number.", code="has_tn")

        super(Form, self).clean()