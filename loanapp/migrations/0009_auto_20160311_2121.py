# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-11 21:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loanapp', '0008_auto_20160311_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loanapp.Account'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='Create new user', max_length=100),
        ),
    ]