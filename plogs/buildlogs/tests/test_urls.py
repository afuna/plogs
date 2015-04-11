from django.test import TestCase
from django.core.urlresolvers import reverse

class BuildLogsTestCase(TestCase):
    def test_project_urls(self):
        """
        Tests the project name in the url using build/new as a proxy
        because it has no additional variables.
        """
        for project_name in ["abc", "ABC", "abc123", "abc-123"]:
            url = reverse('build:new', kwargs={"username": "x", "project_name": project_name})
            self.assertEqual(url, '/people/x/build/%s/new/' % project_name)

    def test_buildlog_urls(self):
        """
        Tests the buildlog view and edit urls
        """
        url = reverse('build:view', kwargs={"username": "x", "project_name": "abc", "log_id": 1})
        self.assertEqual(url, '/people/x/build/abc/1/')

        url = reverse('build:edit', kwargs={"username": "x", "project_name": "abc", "log_id": 1})
        self.assertEqual(url, '/people/x/build/abc/1/edit/')
