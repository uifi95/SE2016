# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyline',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
