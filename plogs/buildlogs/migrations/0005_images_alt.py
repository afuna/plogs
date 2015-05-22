# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0004_buildlogimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildlogimage',
            name='alt',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='buildlogimage',
            name='build',
            field=models.ForeignKey(related_name='images', to='buildlogs.BuildLog', null=True),
            preserve_default=True,
        ),
    ]
