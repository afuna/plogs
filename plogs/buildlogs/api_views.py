from rest_framework import viewsets, permissions
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response

from . import models, serializers

class ProjectViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class ActiveProjectViewSet(viewsets.ViewSet):
    model = models.Project
    permission_classes = (permissions.DjangoModelPermissions,)


    def list(self, request, **kwargs):
        """
        Lists the logged-in user's currently active project
        """
        project = models.Project.objects.latest_for_user(request.user)
        stats = models.BuildLog.statistics.for_project(project)

        data = {
            "project": serializers.ProjectSerializer(project, context={"request": request}).data,

            "stats": stats,

            "build_new_url": reverse('build:new', kwargs={
                "project_name": project.plane.kit.model,
                "username": request.user.username
                }, request=request),

            "expense_new_url": "",
        }

        return Response(data)


class BuildLogViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.BuildLog.objects.all().order_by('-date')
    serializer_class = serializers.BuildLogSerializer
    serializer_detail_class = serializers.BuildLogDetailSerializer
    lookup_field = 'log_id'
