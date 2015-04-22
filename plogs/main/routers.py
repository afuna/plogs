from rest_framework_extensions.routers import NestedRouterMixin
from rest_framework.routers import DefaultRouter

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    """
    Custom router that acts like a DefaultRouter but allows nesting
    of resources.
    """
    pass
