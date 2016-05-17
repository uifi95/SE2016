from django import forms
from django.core.exceptions import ValidationError

from LoginApp.models import Teacher
from StudentApp.models import StudyLine, Year
from django.forms import Form, CharField, ChoiceField, TextInput, IntegerField

from TeacherApp.models import OptionalCourse, PackageToOptionals, OptionalPackage


class OptionalForm(Form):
    name = CharField(max_length=100)
    study_line = ChoiceField(label="Study line", choices=StudyLine.CHOICES)
    year = ChoiceField(label="Year", choices=Year.CHOICES)
    semester = ChoiceField(label="Semester", choices=[(1, 1), (2, 2)])

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Form, self).__init__(*args, **kwargs)

    def clean(self):
        current_teacher = Teacher.objects.filter(user=self.user)

        try:
            if OptionalCourse.objects.filter(name=self.cleaned_data['name'], study_line=self.cleaned_data['study_line'],
                                             year=self.cleaned_data['year'], semester=self.cleaned_data['semester'],
                                             teacher=current_teacher).exists():
                raise ValidationError("Optional already exists.", code="opt_exst")
            if OptionalCourse.objects.filter(teacher=current_teacher).count() == 2:
                raise ValidationError("You can't add more optionals,maximum 2,delete some to add more.",
                                      code="opt_mt_two")
        except KeyError:
            raise ValidationError("No name chosen for optional.", code="no_name")
        super(Form, self).clean()


class GradeForm(Form):
    grade = CharField(max_length=2, widget=TextInput(attrs={'id': 'grade'}))

    def clean(self):
        try:
            if int(self.cleaned_data["grade"]) not in range(1, 11):
                raise ValidationError("Grade must be between 1 and 10", code="gr_val")
        except (ValueError, KeyError):
            raise ValidationError("Grade has to be a number.", code="has_tn")

        super(Form, self).clean()


class PackageForm(Form):
    name = forms.CharField(max_length=30, label="Package name")
    number_of_credits = forms.IntegerField(max_value=8)

    def __init__(self, department, *args, **kwargs):
        opts = OptionalCourse.objects.filter(study_line=department)
        self.opts = []
        for opt in opts:
            if PackageToOptionals.objects.filter(course=opt).count() == 0:
                self.opts.append(opt)
        ropts = []
        for opt in self.opts:
            choiceVal = opt.name + " Teacher: " + opt.teacher.first_name + " " + opt.teacher.last_name + " An: " + str(
                opt.year)
            ropts.append((opt, choiceVal))
        super(Form, self).__init__(*args, **kwargs)
        self.fields['courses'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           choices=ropts, label="Optionals:")

    def clean(self):
        picked = self.cleaned_data["courses"]
        opts = []
        year = None
        semester = None
        try:
            if OptionalPackage.objects.filter(name=self.cleaned_data['name']).exists():
                raise ValidationError("Package already exists.", code="package_exst")
        except KeyError:
            pass
        for p in picked:
            o = OptionalCourse.objects.filter(name=p).first()
            if (year is not None) and year != o.year or (semester is not None and semester != o.semester):
                raise ValidationError("Courses from one package should belong to the same year and semester!",
                                      code="bad_year")

            semester = o.semester
            year = o.year
        super(Form, self).clean()


class TeacherDropDownForm(Form):
    def __init__(self, options, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.ChoiceField(widget=forms.Select(attrs={'onChange': 'this.form.submit();'}),
                                                   choices=options, label="Teacher name:")

        def clean(self):
            super(Form, self).clean()


class GroupDropDownForm(Form):
    def __init__(self, options, selected=0, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        if selected == 0:
            selected = options[0]
        self.fields['group'] = forms.ChoiceField(widget=forms.Select(attrs={'onChange': 'this.form.submit();'}, ),
                                                 choices=options, label="Group Number:", initial=selected)

        def clean(self):
            super(Form, self).clean()
