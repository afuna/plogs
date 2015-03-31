# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildlog',
            name='log_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='buildlog',
            unique_together=set([('project', 'log_id')]),
        ),
    ]
