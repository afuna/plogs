from rest_framework import serializers

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
