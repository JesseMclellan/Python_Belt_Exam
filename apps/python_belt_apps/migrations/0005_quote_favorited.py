# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_belt_apps', '0004_remove_quote_favorited'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='favorited',
            field=models.ManyToManyField(related_name='quotes_liked', to='python_belt_apps.User'),
        ),
    ]
