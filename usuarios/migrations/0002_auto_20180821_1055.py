# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empresa',
            options={'permissions': (('view_empresas', 'Puede Ver Empresas'),)},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'permissions': (('view_usuarios', 'Can view usuario'),)},
        ),
        migrations.AddField(
            model_name='tipoperfil',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tipoperfil',
            name='fecha_desactivacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tipoperfil',
            name='fecha_modificacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_desactivacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_modificacion',
            field=models.DateField(null=True),
        ),
    ]
