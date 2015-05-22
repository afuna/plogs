from rest_framework import viewsets, permissions
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response
import os, urlparse
from boto.s3.connection import S3Connection
from . import models, serializers, api_permissions

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
        }

        return Response(data)


class BuildLogViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [api_permissions.OwnerCanEditPermission]
    queryset = models.BuildLog.objects.all().order_by('-date', '-log_id')
    serializer_class = serializers.BuildLogSerializer
    serializer_detail_class = serializers.BuildLogDetailSerializer
    lookup_field = 'log_id'

    def get_serializer_class(self):
        """
        Use serializer_detail_class when we're editing an object instance
        and when we're creating a new object instance.
        """
        if self.action == "create":
            return self.serializer_detail_class
        return super(BuildLogViewSet, self).get_serializer_class()


class BuildLogImageViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [api_permissions.OwnerCanEditPermission]
    queryset = models.BuildLogImage.objects.all()
    serializer_class = serializers.BuildLogImageSerializer

    def perform_destroy(self, image):
        """
        Delete the image locally and in S3.
        """
        AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        S3_BUCKET = os.environ.get('S3_BUCKET')

        connection = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        bucket = connection.get_bucket(S3_BUCKET)

        url = urlparse.urlparse(image.url)
        key = url.path

        if not key:
            return

        # delete from amazon
        bucket.delete_key(key)

        # delete local reference
        image.delete()


class CategoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'name'


class PartnerViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
    lookup_field = 'name'
