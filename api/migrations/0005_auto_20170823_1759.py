# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170816_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csuser',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='csuser',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='csuser',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
