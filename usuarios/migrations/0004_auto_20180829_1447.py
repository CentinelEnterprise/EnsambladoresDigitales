# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-29 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20180821_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='primer_login',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='tipo_empresa',
            field=models.SmallIntegerField(choices=[(1, 'Sin Asignar'), (2, 'Aplicacion'), (3, 'Directorio Activo')], default=1),
        ),
    ]