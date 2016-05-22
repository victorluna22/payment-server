# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_auto_20160522_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paypal_code',
            field=models.CharField(default='123123123123', max_length=255, verbose_name=b'C\xc3\xb3digo Paypal'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='is_authorized',
            field=models.BooleanField(default=0, verbose_name=b'Aut.'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=0, verbose_name=b'Pago'),
        ),
    ]
