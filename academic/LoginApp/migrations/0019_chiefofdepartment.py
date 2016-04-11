# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0018_remove_student_study_line'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChiefOfDepartment',
            fields=[
                ('teacher_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='LoginApp.Teacher')),
            ],
            bases=('LoginApp.teacher',),
        ),
    ]
