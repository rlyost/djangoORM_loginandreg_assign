# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-22 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
