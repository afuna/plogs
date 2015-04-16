from rest_framework.reverse import reverse
from rest_framework import serializers

from plogs.main.serializers import UserSerializer
from . import models

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='plane.owner.username')
    name = serializers.ReadOnlyField(source='plane.kit.model')

    # resource urls
    api_url = serializers.SerializerMethodField()
    buildlogs_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = ('id', 'name', 'date_started', 'user', 'api_url', 'buildlogs_url')

    def get_api_url(self, obj):
        """
        Return the URL for the detail view of this project.
        """
        return reverse('api.build:user-projects-detail',
                       args=[obj.plane.owner.username,
                             obj.id,
                             "json",
                            ],
                        request=self.context['request'])

    def get_buildlogs_url(self, obj):
        """
        Return the URL for the list view of buildlogs related to this project.
        """
        return reverse('api.build:project-buildlogs-list',
                       args=[obj.plane.owner.username,
                             obj.id,
                             "json",
                            ],
                        request=self.context['request'])

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = ('id', 'name')

class BuildLogSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    category = CategorySerializer()
    partner = PartnerSerializer()

    # resource urls
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = models.BuildLog
        fields = ('log_id', 'project', 'category', 'partner', 'date',
                  'duration', 'reference', 'parts', 'summary', 'notes',
                  'api_url')

    def get_api_url(self, obj):
        """
        Return the URL for the detail view of this buildlog.
        """
        return reverse('api.build:project-buildlogs-detail',
                       args=[obj.project.plane.owner.username,
                             obj.project.id,
                             obj.log_id,
                             "json",
                            ],
                        request=self.context['request'])
