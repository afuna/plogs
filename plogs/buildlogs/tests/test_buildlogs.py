from django.test import TestCase
from django.contrib.auth.models import User
from plogs.planes.models import Plane, Engine, Kit, Prop
from ..models import BuildLog, BuildLogImage, Project, Category
from datetime import date

class BuildLogTestCase(TestCase):
    @classmethod
    def create_project(cls, name=u"kit"):
        if not hasattr(cls, 'user_count'):
            cls.user_count = 0

        kit = Kit.objects.create(model=u"%s %s" % (name, cls.user_count))
        engine = Engine.objects.create()
        prop = Prop.objects.create()
        user, _ = User.objects.get_or_create(username=str(cls.user_count))
        plane = Plane.objects.create(kit=kit,
                                     engine=engine,
                                     prop=prop,
                                     owner=user
                                    )

        cls.user_count += 1
        return Project.objects.create(plane=plane)

    @classmethod
    def create_buildlog(cls):
        project = BuildLogTestCase.create_project()
        category, _ = Category.objects.get_or_create(name=u"category", user=project.plane.owner)

        buildlog = BuildLog.objects.create(
            project = project,
            category = category,
            date = date.today()
        )
        return buildlog

    def test_create_buildlog(self):
        buildlog1 = BuildLogTestCase.create_buildlog()
        self.assertIsInstance(buildlog1, BuildLog)
        self.assertEqual(buildlog1.log_id, 1, "log_id for project1 is 1")

        # different owner, different project
        buildlog2 = BuildLogTestCase.create_buildlog()
        self.assertIsInstance(buildlog2, BuildLog)
        self.assertEqual(buildlog2.log_id, 1, "log_id for project2 is 1")

        # same owner, same project
        buildlog3 = BuildLog.objects.create(
            project = buildlog2.project,
            category = buildlog2.category,
            date = date.today()
        )
        self.assertIsInstance(buildlog3, BuildLog)
        self.assertEqual(buildlog3.log_id, 2, "log_id for project2 is 2")

    def test_statistics(self):
        project = BuildLogTestCase.create_project()
        stats = BuildLog.statistics.for_project(project)
        self.assertEqual(stats["hours"], 0)
        self.assertEqual(stats["sessions"], 0)
        self.assertEqual(stats["dollars"], 0)

        BuildLog.objects.create(
            project = project,
            category = Category.objects.create(name=u"a", user=project.plane.owner),
            date = date.today(),
            duration = 3.5,
        )
        BuildLog.objects.create(
            project = project,
            category = Category.objects.create(name=u"b", user=project.plane.owner),
            date = date.today(),
            duration = 1.25,
        )
        stats = BuildLog.statistics.for_project(project)
        self.assertEqual(stats["hours"], 4.75)
        self.assertEqual(stats["sessions"], 2)
        self.assertEqual(stats["dollars"], 0)

class BuildLogImageTestCase(TestCase):
    @classmethod
    def create_project(cls, name=u"kit"):
        if not hasattr(cls, 'user_count'):
            cls.user_count = 0

        kit = Kit.objects.create(model=u"%s %s" % (name, cls.user_count))
        engine = Engine.objects.create()
        prop = Prop.objects.create()
        user, _ = User.objects.get_or_create(username=str(cls.user_count))
        plane = Plane.objects.create(kit=kit,
                             engine=engine,
                             prop=prop,
                             owner=user
                            )

        cls.user_count += 1
        return Project.objects.create(plane=plane)

    @classmethod
    def create_buildlog(cls):
        project = BuildLogTestCase.create_project()
        category, _ = Category.objects.get_or_create(name=u"category", user=project.plane.owner)

        buildlog = BuildLog.objects.create(
            project = project,
            category = category,
            date = date.today()
        )
        return buildlog

    def test_create_images(self):
        buildlog = BuildLogImageTestCase.create_buildlog()
        image1 = BuildLogImage.objects.create(project=buildlog.project, build=buildlog, url="http://example.com/example.jpg", caption="yo")
        self.assertIsInstance(image1, BuildLogImage)
        self.assertEqual(image1.id, 1)
        self.assertEqual(image1.image_id, 1, "image_id for image1 is 1")

        # different owner, different project
        buildlog2 = BuildLogImageTestCase.create_buildlog()
        image2 = BuildLogImage.objects.create(project=buildlog2.project, build=buildlog2, url="http://example.com/example.jpg", caption="yo")
        self.assertIsInstance(image2, BuildLogImage)
        self.assertEqual(image2.id, 2)
        self.assertEqual(image2.image_id, 1, "image_id for image2 is 1")

        # same owner, same project
        image3 = BuildLogImage.objects.create(project=buildlog2.project, build=buildlog2, url="http://example.com/example.jpg", caption="yo")
        self.assertIsInstance(image3, BuildLogImage)
        self.assertEqual(image3.id, 3)
        self.assertEqual(image3.image_id, 2, "log_id for project2 is 2")

    def test_list_images(self):
        buildlog1 = BuildLogImageTestCase.create_buildlog()
        project1 = buildlog1.project
        buildlog2 = BuildLogImageTestCase.create_buildlog()
        project2 = buildlog2.project

        image1 = BuildLogImage.objects.create(project=project1, url="...", caption="project1 unassociated #1")
        image2 = BuildLogImage.objects.create(project=project1, url="...", caption="project1 unassociated #2")
        image3 = BuildLogImage.objects.create(project=project1, build=buildlog1, url="...", caption="project1 associated #1")
        image4 = BuildLogImage.objects.create(project=project2, url="...", caption="project2 unassociated #1")
        image5 = BuildLogImage.objects.create(project=project2, url="...", caption="project2 associated #1", build=buildlog2)

        unassociated_images1 = BuildLogImage.objects.from_build_new(project1)
        self.assertEquals(len(unassociated_images1), 2)
        associated_images1 = BuildLogImage.objects.for_build(buildlog1)
        self.assertEquals(len(associated_images1), 1)

        unassociated_images2 = BuildLogImage.objects.from_build_new(project2)
        self.assertEquals(len(unassociated_images2), 1)
        associated_images2 = BuildLogImage.objects.for_build(buildlog2)
        self.assertEquals(len(associated_images2), 1)



