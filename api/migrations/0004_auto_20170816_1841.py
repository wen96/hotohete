# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_hotohetesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csuser',
            name='steam_id',
            field=models.CharField(blank=True, max_length=126, null=True),
        ),
    ]