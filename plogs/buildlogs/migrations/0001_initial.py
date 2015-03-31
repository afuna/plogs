# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('duration', models.PositiveSmallIntegerField(verbose_name=b'hours', blank=True)),
                ('reference', models.CharField(max_length=255, verbose_name=b'manual section', blank=True)),
                ('parts', models.CharField(max_length=255, verbose_name=b'parts reference', blank=True)),
                ('summary', models.CharField(max_length=255, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_started', models.DateField(auto_now_add=True)),
                ('plane', models.ForeignKey(to='planes.Plane')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='buildlog',
            name='category',
            field=models.ForeignKey(to='buildlogs.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buildlog',
            name='partner',
            field=models.ForeignKey(blank=True, to='buildlogs.Partner', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buildlog',
            name='project',
            field=models.ForeignKey(to='buildlogs.Project'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='buildlog',
            name='parts',
            field=models.CharField(max_length=255, verbose_name=b'part numbers', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='partner',
            unique_together=set([('user', 'name')]),
        ),
    ]
