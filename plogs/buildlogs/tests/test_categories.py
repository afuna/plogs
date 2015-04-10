from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User
from ..models import Category

class CategoryTestCase(TestCase):
    def test_create_category(self):
        """Create a category."""
        user = User.objects.create(username="1")
        category = Category.objects.create(user=user, name="category")
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, "category")
        self.assertIs(category.user, user)

    def test_unique_category(self):
        """Test category names are unique for each user."""
        user1 = User.objects.create(username="test_unique_category_1")
        user2 = User.objects.create(username="test_unique_category_2")

        category1 = Category.objects.create(user=user1, name="category1")
        self.assertEqual(category1.name, "category1")

        # FIXME: handle duplicate category names better
        with transaction.atomic(), self.assertRaises(IntegrityError):
            Category.objects.create(user=user1, name="category1")

        category2 = Category.objects.create(user=user2, name="category1")
        self.assertEqual(category2.name, "category1")


class CategoryListTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1")
        Category.objects.create(user=user1, name="user1_foo")
        Category.objects.create(user=user1, name="user1_bar")

        user2 = User.objects.create(username="user2")
        Category.objects.create(user=user2, name="user2_foo")

    def test_list_categories_by_user(self):
        """Test list categories by user."""
        user1 = User.objects.filter(username="user1")
        user1_categories = Category.objects.for_user(user1).order_by("id")
        self.assertEquals(len(user1_categories), 2)
        self.assertEquals(user1_categories[0].name, "user1_foo")
        self.assertEquals(user1_categories[1].name, "user1_bar")

        user2 = User.objects.filter(username="user2")
        user2_categories = Category.objects.for_user(user2)
        self.assertEquals(len(user2_categories), 1)
        self.assertEquals(user2_categories[0].name, "user2_foo")

