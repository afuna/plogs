from rest_framework import serializers
from markdown import markdown

from .markdown_extensions import ImageFigureExtension
from .utils import sanitize


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
        Convert markdown to sanitized HTML.
        """
        value = super(MarkdownField, self).to_representation(value)
        value = markdown(value, output_format='html5', extensions=[ImageFigureExtension()])
        return sanitize(value)


class FakeArrayField(serializers.CharField):
    """
    Returns an array for the serialized format, but stores as a comma-separated string.
    """
    def to_representation(self, value):
        return [str(s).strip() for s in value.split(',')]