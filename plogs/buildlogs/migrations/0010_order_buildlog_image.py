# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0009_project_slug_slugify'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buildlogimage',
            options={'ordering': ('id',)},
        ),
    ]
