# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

def project_slug_slugify(apps, schema_editor):
    Project = apps.get_model('buildlogs', 'Project')
    for project in Project.objects.all():
        project.slug = slugify(project.slug)
        project.save()

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0008_project_slug_post_populate'),
    ]

    operations = [
        migrations.RunPython(project_slug_slugify, reverse_code=noop),
    ]
