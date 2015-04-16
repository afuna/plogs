from django.test import TestCase
from django.contrib.auth.models import User
from plogs.planes import models as plane_models
from .. import models, serializers
from datetime import date

class ProjectSerializerTestCase(TestCase):
    """
    Test serialization of project model
    """
    def setUp(self):
        kit = plane_models.Kit(model='acme')
        kit.save()

        engine = plane_models.Engine()
        engine.save()

        prop = plane_models.Prop()
        prop.save()

        owner = User(username='project_serializer_owner')
        owner.save()

        plane = plane_models.Plane(kit=kit, engine=engine, prop=prop, owner=owner)
        plane.save()

        self.project = models.Project(plane=plane)
        self.project.save()

    def test_project_serializer_representation(self):
        """
        Tests serialized representation of a project object.
        """

        serializer = serializers.ProjectSerializer(self.project)
        data = serializer.data

        self.assertEqual(len(data), 6, "Got correct number of fields in serialized data.")

        self.assertTrue('id' in data, 'Got project id.')
        self.assertTrue('date_started' in data, 'Got project start date.')
        self.assertEqual(data['user'], 'project_serializer_owner', 'Got project user name.')
        self.assertEqual(data['name'], 'acme', 'Got project name.')
        self.assertRegexpMatches(data['api_url'], '/api/people/project_serializer_owner/projects/\d+', 'Got api url')


class BuildLogSerializerTestCase(TestCase):
    """
    Test serialization of buildlog model
    """
    def setUp(self):
        kit = plane_models.Kit(model='acme')
        kit.save()

        engine = plane_models.Engine()
        engine.save()

        prop = plane_models.Prop()
        prop.save()

        owner = User(username='project_serializer_owner')
        owner.save()

        plane = plane_models.Plane(kit=kit, engine=engine, prop=prop, owner=owner)
        plane.save()

        project = models.Project(plane=plane)
        project.save()

        category = models.Category(user=owner, name="foo")
        category.save()

        partner = models.Partner(user=owner, name="baz")
        partner.save()

        self.buildlog = models.BuildLog(project=project,
                                        category=category,
                                        partner=partner,
                                        date=date.today(),
                                        duration=2.5,
                                        reference='XYZ',
                                        parts='ABC',
                                        summary='test test',
                                        notes='testing testing 123'
                                       )
        self.buildlog.save()

    def test_buildlog_serializer_representation(self):
        """
        Tests serialized representation of a buildlog object.
        """
        serializer = serializers.BuildLogSerializer(self.buildlog)
        data = serializer.data

        self.assertEqual(len(data), 11, "Got correct number of fields in serialized data.")
        self.assertEqual(data['log_id'], 1, "Buildlog log_id")
        self.assertEqual(data['project']['name'], 'acme', "Buildlog project name")
        self.assertEqual(data['category']['name'], 'foo', "Buildlog category name")
        self.assertEqual(data['partner']['name'], 'baz', "Buildlog partner name")
        self.assertEqual(data['date'], str(date.today()), "Buildlog date")
        self.assertEqual(data['duration'], '2.50', "Buildlog duration")
        self.assertEqual(data['reference'], "XYZ", "Buildlog reference")
        self.assertEqual(data['parts'], "ABC", "Buildlog parts")
        self.assertEqual(data['summary'], "test test", "Buildlog summary")
        self.assertEqual(data['notes'], "testing testing 123", "Buildlog notes")
        self.assertEqual(data['api_url'], '', "Buildlog api_url")
