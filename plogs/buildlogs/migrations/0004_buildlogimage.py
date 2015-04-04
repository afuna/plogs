# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0003_auto_20150331_0504'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildLogImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('caption', models.CharField(max_length=255, blank=True)),
                ('image_id', models.PositiveIntegerField()),
                ('build', models.ForeignKey(to='buildlogs.BuildLog', null=True)),
                ('project', models.ForeignKey(to='buildlogs.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
