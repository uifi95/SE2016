# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0004_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='year',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], verbose_name='Year'),
        ),
    ]