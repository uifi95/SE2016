# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherApp', '0009_auto_20160328_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='study_line',
            field=models.CharField(choices=[('Informatics', 'Informatics'), ('Mathematics', 'Mathematics'), ('Mathematics & Informatics', 'Mathematics & Informatics')], max_length=50),
        ),
    ]
