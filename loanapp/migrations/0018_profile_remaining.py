# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanapp', '0017_auto_20161202_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='remaining',
            field=models.DecimalField(decimal_places=2, default=b'0.0', max_digits=10),
        ),
    ]
