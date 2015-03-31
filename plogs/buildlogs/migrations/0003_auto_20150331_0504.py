# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0002_auto_20150331_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildlog',
            name='duration',
            field=models.DecimalField(verbose_name=b'hours', max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
