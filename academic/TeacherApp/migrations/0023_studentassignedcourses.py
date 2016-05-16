# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0023_student_is_enrolled'),
        ('TeacherApp', '0022_auto_20160515_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAssignedCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeacherApp.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LoginApp.Student')),
            ],
        ),
    ]