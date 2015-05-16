from rest_framework.reverse import reverse
from rest_framework import serializers

from . import models
from .fields import GetOrCreateSlugRelatedField, MarkdownField


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
                             "json"],
                       request=self.context['request'])

    def get_buildlogs_url(self, obj):
        """
        Return the URL for the list view of buildlogs related to this project.
        """
        return reverse('api.build:project-buildlogs-list',
                       args=[obj.plane.owner.username,
                             obj.id,
                             "json"],
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
    category = GetOrCreateSlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='name'
    )
    partner = GetOrCreateSlugRelatedField(
        queryset=models.Partner.objects.all(),
        slug_field='name',
        required=False
    )

    # system-generated
    log_id = serializers.IntegerField(required=False, read_only=True)

    # resource urls
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = models.BuildLog
        fields = ('log_id', 'project', 'category', 'partner', 'date',
                  'duration', 'reference', 'parts', 'summary', 'api_url')

    def get_api_url(self, obj):
        """
        Return the URL for the detail view of this buildlog.
        """
        return reverse('api.build:project-buildlogs-detail',
                       args=[obj.project.plane.owner.username,
                             obj.project.id,
                             obj.log_id,
                             "json"],
                       request=self.context['request'])

    def validate_project(self, value):
        """
        Return a project object using the given project data.
        """
        project_data = self.initial_data['project']
        return models.Project.objects.for_user(self.context['request'].user).get(id=project_data['id'])

    def validate_reference(self, value):
        """
        Convert the array of reference numbers into a comma-separated string.
        """
        return ', '.join(self.initial_data["reference"])

    def validate_parts(self, value):
        """
        Convert the array of part numbers into a comma-separated string.
        """
        return ', '.join(self.initial_data["parts"])


class BuildLogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BuildLogImage
        fields = ('url', 'caption')


class BuildLogDetailSerializer(BuildLogSerializer):
    images = BuildLogImageSerializer(many=True, read_only=True)
    notes = MarkdownField(required=False)

    class Meta(BuildLogSerializer.Meta):
        fields = ('log_id', 'project', 'category', 'partner', 'date',
                  'duration', 'reference', 'parts', 'summary', 'api_url',
                  'notes', 'images')

        # disable automatic validators -- the UniqueTogetherValidation
        # for log_id was causing log_id to be required on post (we'll set it later)
        validators = []

    def create(self, validated_data):
        """
        Override the default create to save images on the buildlog.
        """

        buildlog = models.BuildLog.objects.create(**validated_data)

        images = models.BuildLogImage.objects.from_build_new(buildlog.project)
        for image in images:
            image.build = buildlog
            image.save()

        return buildlog
