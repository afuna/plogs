# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def project_slug_from_plane(apps, schema_editor):
    Project = apps.get_model('buildlogs', 'Project')
    for project in Project.objects.all():
        project.slug = project.plane.kit.model
        project.user = project.plane.owner
        project.save()

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('buildlogs', '0006_project_slug_init'),
    ]

    operations = [
        migrations.RunPython(project_slug_from_plane, reverse_code=noop),
    ]
