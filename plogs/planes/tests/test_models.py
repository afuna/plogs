from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Kit, Engine, Prop, Plane
import uuid

class KitTestCase(TestCase):
    def setUp(self):
        Kit.objects.create()
        Kit.objects.create(manufacturer="a",
                           model="M",
                           serial_number="123",
                           registration_number="456",
                          )


    def test_kit_representation(self):
        """Check kit representation"""
        empty_kit = Kit.objects.get(manufacturer="")
        self.assertEqual("%s" % empty_kit, "<Kit #%d>" % empty_kit.id)

        filledin_kit = Kit.objects.get(manufacturer="a")
        self.assertEqual("%s" % filledin_kit, "M #123")


class EngineTestCase(TestCase):
    def setUp(self):
        Engine.objects.create()
        Engine.objects.create(manufacturer="a",
                              model="M",
                              horsepower="42",
                              serial_number="123",
                             )


    def test_engine_representation(self):
        """Check engine representation"""
        empty_engine = Engine.objects.get(manufacturer="")
        self.assertEqual("%s" % empty_engine, "<Engine #%d>" % empty_engine.id)

        filledin_engine = Engine.objects.get(manufacturer="a")
        self.assertEqual("%s" % filledin_engine, "M 42 HP #123")


class PropTestCase(TestCase):
    def setUp(self):
        Prop.objects.create()
        Prop.objects.create(manufacturer="a",
                              model="M",
                              serial_number="123",
                              prop_type="FP"
                             )


    def test_prop_representation(self):
        """Check prop representation"""
        empty_prop = Prop.objects.get(manufacturer="")
        self.assertEqual("%s" % empty_prop, "<Prop #%d>" % empty_prop.id)

        filledin_prop = Prop.objects.get(manufacturer="a")
        self.assertEqual("%s" % filledin_prop, "M Fixed Pitch #123")


class PlaneTestCase(TestCase):
    def setUp(self):
        Plane.objects.create(**self.create_plane_components())

    def create_plane_components(self):
        random_username = str(uuid.uuid4())[:30]
        return { "owner": User.objects.create(username=random_username),
                 "kit": Kit.objects.create(),
                 "engine": Engine.objects.create(),
                 "prop": Prop.objects.create()
                }

    def test_empty_plane(self):
        """Test that we can create a plane without filling in the engine, etc
        information"""
        plane = Plane.objects.create(**self.create_plane_components())
        self.assertIsInstance(plane, Plane)

    def test_plane_representation(self):
        """Check plane representation"""
        plane = Plane.objects.first()
        self.assertEqual("%s" % plane , "%s" % plane.kit)
