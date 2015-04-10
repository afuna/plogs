from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User
from ..models import Partner

class PartnerTestCase(TestCase):
    def test_create_partner(self):
        """Create a partner."""
        user = User.objects.create(username="1")
        partner = Partner.objects.create(user=user, name="partner")
        self.assertIsInstance(partner, Partner)
        self.assertEqual(partner.name, "partner")
        self.assertIs(partner.user, user)

    def test_unique_partner(self):
        """Test partner names are unique for each user."""
        user1 = User.objects.create(username="test_unique_partner_1")
        user2 = User.objects.create(username="test_unique_partner_2")

        partner1 = Partner.objects.create(user=user1, name="partner1")
        self.assertEqual(partner1.name, "partner1")

        # FIXME: handle duplicate partner names better
        with transaction.atomic(), self.assertRaises(IntegrityError):
            Partner.objects.create(user=user1, name="partner1")

        partner2 = Partner.objects.create(user=user2, name="partner1")
        self.assertEqual(partner2.name, "partner1")


class PartnerListTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1")
        Partner.objects.create(user=user1, name="user1_foo")
        Partner.objects.create(user=user1, name="user1_bar")

        user2 = User.objects.create(username="user2")
        Partner.objects.create(user=user2, name="user2_foo")

    def test_list_categories_by_user(self):
        """Test list categories by user."""
        user1 = User.objects.filter(username="user1")
        user1_categories = Partner.objects.for_user(user1).order_by("id")
        self.assertEquals(len(user1_categories), 2)
        self.assertEquals(user1_categories[0].name, "user1_foo")
        self.assertEquals(user1_categories[1].name, "user1_bar")

        user2 = User.objects.filter(username="user2")
        user2_categories = Partner.objects.for_user(user2)
        self.assertEquals(len(user2_categories), 1)
        self.assertEquals(user2_categories[0].name, "user2_foo")

