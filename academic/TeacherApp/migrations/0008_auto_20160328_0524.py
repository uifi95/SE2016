# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherApp', '0007_auto_20160328_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('name', 'teacher', 'study_line')]),
        ),
    ]