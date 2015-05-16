from django.conf import settings
from rest_framework import serializers
import bleach
from markdown import markdown

from .markdown_extensions import ImageFigureExtension


class GetOrCreateSlugRelatedField(serializers.SlugRelatedField):
    """
        Get by the slug and the queryset provided.
        If object with slug does not yet exist, create it.
    """
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{
                    self.slug_field: data,
                    "user": self.context['request'].user
            })
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class MarkdownField(serializers.CharField):

    """
    Serializes text that contains Markdown for display
    """
    def to_representation(self, value):
        """
        Add linebreaks to the text for display as HTML.
        """
        value = super(MarkdownField, self).to_representation(value)
        return bleach.clean(
            markdown(value, output_format='html5', extensions=[ImageFigureExtension()]),
            tags=settings.BLEACH_ALLOWED_TAGS,
            attributes=settings.BLEACH_ALLOWED_ATTRIBUTES
        )


class FakeArrayField(serializers.CharField):
    """
    Returns an array for the serialized format, but stores as a comma-separated string.
    """
    def to_representation(self, value):
        return [str(s).strip() for s in value.split(',')]