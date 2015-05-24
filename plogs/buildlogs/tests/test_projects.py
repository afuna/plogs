from django.test import TestCase
from django.contrib.auth.models import User
from plogs.planes.models import Plane, Kit, Engine, Prop
from ..models import Project
from datetime import date

class ProjectTestCase(TestCase):
    def setUp(self):
        kit = Kit.objects.create(model=u"kit")
        engine = Engine.objects.create()
        prop = Prop.objects.create()
        user = User.objects.create()
        Plane.objects.create(kit=kit,
                             engine=engine,
                             prop=prop,
                             owner=user
                            )

    def test_create_project(self):
        """Test project creation."""
        plane = Plane.objects.last()
        project = Project.objects.create(plane=plane)
        self.assertEqual(str(project), project.plane.kit.model)
        self.assertEqual(project.date_started, date.today())

class ProjectListTestCase(TestCase):
    @classmethod
    def create_plane(cls, name=u"kit", username=u"username"):
        kit = Kit.objects.create(model=name)
        engine = Engine.objects.create()
        prop = Prop.objects.create()
        user, _ = User.objects.get_or_create(username=username)
        plane = Plane.objects.create(kit=kit,
                             engine=engine,
                             prop=prop,
                             owner=user
                            )
        return plane

    def setUp(self):
        plane1 = ProjectListTestCase.create_plane(name=u"kit1", username=u"1")
        plane2 = ProjectListTestCase.create_plane(name=u"kit1", username=u"2")
        plane3 = ProjectListTestCase.create_plane(name=u"kit2", username=u"2")

        Project.objects.create(plane=plane1)
        Project.objects.create(plane=plane2)
        Project.objects.create(plane=plane3)

    def test_list_projects_by_user(self):
        """Test listing of projects"""
        project1, project2, project3 = Project.objects.all().order_by("id")

        project1 = Project.objects.for_user(user=project1.plane.owner)
        self.assertEqual(len(project1), 1)
        self.assertEqual(str(project1.first()), "kit1")

        project2 = Project.objects.for_user(user=project2.plane.owner).order_by("id")
        self.assertEqual(len(project2), 2)
        self.assertEqual(str(project2[0]), "kit1")
        self.assertEqual(str(project2[1]), "kit2")

    def test_list_specific_project(self):
        """Test fetching a specific project by name"""
        project1, project2, project3 = Project.objects.all().order_by("id")

        named_project = Project.objects.for_user(user=project2.plane.owner, project_name=u"kit1")
        self.assertEqual(len(named_project), 1)
        self.assertEqual(named_project.first().plane.owner, project2.plane.owner)
        self.assertEqual(str(named_project.first()), "kit1")

    # FIXME: needs to use actual active, not just last created
    def test_get_active_project(self):
        """Test getting the user's currently active project"""
        project1, project2, project3 = Project.objects.all().order_by("id")

        active_project_user1 = Project.objects.latest_for_user(project1.plane.owner)
        self.assertEqual(str(active_project_user1), "kit1")

        # project 2 (kit1)'s user's actual active project is kit2
        active_project_user2 = Project.objects.latest_for_user(project2.plane.owner)
        self.assertEqual(str(active_project_user2), "kit2")
