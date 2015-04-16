from rest_framework import viewsets, permissions
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.contrib.auth.models import User
from . import serializers

class UserViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
