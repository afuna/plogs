from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Kit, Engine, Prop, Plane

class PlaneListTestCase(TestCase):
    def create_plane_components(self, username):
        return { "owner": User.objects.create(username=username),
                 "kit": Kit.objects.create(),
                 "engine": Engine.objects.create(),
                 "prop": Prop.objects.create()
                }

    def setUp(self):
        Plane.objects.create(**self.create_plane_components("1"))

        # user 2 has 2 planes
        plane1 = self.create_plane_components("2")
        plane2 = self.create_plane_components("x")
        plane2["owner"] = plane1["owner"]

        Plane.objects.create(**plane1)
        Plane.objects.create(**plane2)

    def test_list_all_planes(self):
        all_planes = Plane.objects.get_queryset()
        self.assertEquals(len(all_planes), 3)

    def test_list_planes_by_owner(self):
        owner1 = User.objects.filter(username="1")
        owner1_planes = Plane.objects.for_user(owner1)
        self.assertEquals(len(owner1_planes), 1)

        owner2 = User.objects.filter(username="2")
        owner2_planes = Plane.objects.for_user(owner2)
        self.assertEquals(len(owner2_planes), 2)