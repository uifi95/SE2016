# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 02:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherApp', '0008_auto_20160328_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='study_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentApp.StudyLine'),
        ),
    ]
