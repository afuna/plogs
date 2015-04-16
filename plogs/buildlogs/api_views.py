from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from . import models, serializers

class ProjectViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

class BuildLogViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.BuildLog.objects.all()
    serializer_class = serializers.BuildLogSerializer
    lookup_field = 'log_id'
