# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20160220_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='softwareconfiguration',
            name='arch',
            field=models.CharField(choices=[('32', '32-bit'), ('64', '64-bit'), ('both', 'both')], default='64', max_length=10),
        ),
    ]