# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufacturer', models.CharField(max_length=255, blank=True)),
                ('model', models.CharField(max_length=255, blank=True)),
                ('horsepower', models.CharField(max_length=255, blank=True)),
                ('serial_number', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufacturer', models.CharField(max_length=255, blank=True)),
                ('model', models.CharField(max_length=255, blank=True)),
                ('serial_number', models.CharField(max_length=255, blank=True)),
                ('registration_number', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engine', models.ForeignKey(to='planes.Engine')),
                ('kit', models.ForeignKey(to='planes.Kit')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufacturer', models.CharField(max_length=255, blank=True)),
                ('model', models.CharField(max_length=255, blank=True)),
                ('serial_number', models.CharField(max_length=255, blank=True)),
                ('prop_type', models.CharField(max_length=2, choices=[(b'FP', b'Fixed pitch'), (b'CS', b'Constant speed')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='plane',
            name='prop',
            field=models.ForeignKey(to='planes.Prop'),
            preserve_default=True,
        ),
    ]
