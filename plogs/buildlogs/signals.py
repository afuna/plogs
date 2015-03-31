from django.dispatch import receiver
from plogs.planes.signals import post_create
from plogs.planes.models import Plane
from .models import Project

@receiver(post_create, sender=Plane)
def plane_post_create(sender, **kwargs):
    project = Project(plane=kwargs["plane"])
    project.save()
