from django.conf import settings
import bleach

def sanitize(value):
    """
    Sanitize HTML output.
    """
    return bleach.clean(
        value,
        tags=settings.BLEACH_ALLOWED_TAGS,
        attributes=settings.BLEACH_ALLOWED_ATTRIBUTES
    )
