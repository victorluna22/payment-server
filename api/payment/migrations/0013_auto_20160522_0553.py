# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_payment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_authorized',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=1),
        ),
    ]
