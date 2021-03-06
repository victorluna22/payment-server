# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-04 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20160504_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='cpf',
            field=models.CharField(default='', max_length=14, verbose_name=b'CPF'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='installments',
            field=models.IntegerField(default=1, verbose_name=b'Parcelas'),
        ),
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name=b'Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='targetprovider',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xc3\x9altima atualiza\xc3\xa7\xc3\xa3o'),
        ),
    ]
