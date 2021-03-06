# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20180821_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='fecha_inicio_empresa',
        ),
        migrations.AddField(
            model_name='empresa',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='fecha_desactivacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='fecha_modificacion',
            field=models.DateField(null=True),
        ),
    ]
