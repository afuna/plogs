from django.test import TestCase
from django.contrib.auth.models import User
from .. import models, serializers

class PlaneSerializerTestCase(TestCase):
    """
    Test serialization of plane model
    """
    def setUp(self):
        kit = models.Kit(manufacturer='abc',
                         model='123',
                         serial_number='123',
                         registration_number='123')
        kit.save()

        engine = models.Engine(manufacturer='xyz',
                               model='000',
                               horsepower='100',
                               serial_number='123')
        engine.save()

        prop = models.Prop(manufacturer='foo',
                           model='bar',
                           prop_type='FP',
                           serial_number='123')
        prop.save()

        owner = User(username='plane_serializer_owner')
        owner.save()

        self.plane = models.Plane(kit=kit, engine=engine, prop=prop, owner=owner)
        self.plane.save()

    def test_plane_serializer_representation(self):
        """
        Tests serialized representation of a plane object.
        """

        serializer = serializers.PlaneSerializer(self.plane)
        plane = serializer.data

        self.assertEquals(len(plane), 4, "4 fields in serialized plane.")

        self.assertTrue('id' in plane['owner'], 'Got plane owner id.')
        self.assertEqual(plane['owner']['username'], 'plane_serializer_owner', 'Got plane owner username.')

        self.assertDictEqual(
            plane['engine'],
            { 'manufacturer': 'xyz', 'model': '000', 'horsepower': '100', 'serial_number': '123'},
            'Got serialized plane engine.'
        )

        self.assertDictEqual(
            plane['kit'],
            { 'manufacturer': 'abc', 'model': '123', 'serial_number': '123', 'registration_number': '123'},
            'Got serialized plane kit.'
        )

        self.assertDictEqual(
            plane['prop'],
            { 'manufacturer': 'foo', 'model': 'bar', 'serial_number': '123', 'prop_type': 'FP'}
        )
