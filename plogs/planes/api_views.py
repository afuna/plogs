from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from . import models, serializers

class UserPlaneViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Plane.objects.all()
    serializer_class = serializers.PlaneSerializer


