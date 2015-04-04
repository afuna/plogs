# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prop',
            name='prop_type',
            field=models.CharField(max_length=2, choices=[(b'FP', b'Fixed Pitch'), (b'CS', b'Constant Speed')]),
            preserve_default=True,
        ),
    ]
