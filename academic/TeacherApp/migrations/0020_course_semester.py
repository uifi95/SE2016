# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherApp', '0019_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.IntegerField(choices=[(1, 1), (2, 2)], default=1, verbose_name='Semester'),
        ),
    ]