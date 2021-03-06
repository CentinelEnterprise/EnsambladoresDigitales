# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-14 20:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion_empresa', models.CharField(max_length=200, unique=True)),
                ('razon_social_empresa', models.CharField(max_length=200)),
                ('nombre_comercial_empresa', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo_empresa', models.SmallIntegerField(choices=[(1, 'Sin Definir'), (2, 'Natural'), (3, 'Juridica')], default=1)),
                ('estado_empresa', models.BooleanField(default=True)),
                ('observaciones_empresa', models.CharField(max_length=3000, null=True)),
                ('fecha_inicio_empresa', models.DateField()),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'permissions': (('view_proveedores', 'Can view proveedores'),),
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_perfil', models.CharField(max_length=200)),
                ('observaciones', models.CharField(blank=True, max_length=200, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'permissions': (('view_perfil', 'Can view perfiles'),),
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
                ('id_perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='TipoPerfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo_perfil', models.CharField(max_length=200)),
                ('descripcion_tipo_perfil', models.CharField(blank=True, max_length=200, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'permissions': (('view_tipoperfil', 'Can view Tipo perfiles'),),
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=200)),
                ('identificacion', models.PositiveIntegerField()),
                ('nombre', models.CharField(max_length=350)),
                ('email', models.EmailField(max_length=254)),
                ('activo', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Empresa')),
                ('tipo_perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.TipoPerfil')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'permissions': (('view_usuario', 'Can view usuario'),),
            },
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='tipo_perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.TipoPerfil'),
        ),
    ]
