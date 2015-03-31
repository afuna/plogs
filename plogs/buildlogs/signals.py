from django.dispatch import receiver
from plogs.main.signals import post_create as post_create_user
from plogs.planes.signals import post_create as post_create_plane
from django.contrib.auth.models import User
from plogs.planes.models import Plane
from .models import Project, Category

@receiver(post_create_plane, sender=Plane)
def create_project_for_plane(sender, **kwargs):
    project = Project(plane=kwargs["plane"])
    project.save()

@receiver(post_create_user, sender=User)
def prepopulate_user_categories(sender, **kwargs):
    user = kwargs['user']
    for name in Category.default_categories():
        category = Category(user=user, name=name)
        category.save()
