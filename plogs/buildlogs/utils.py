from django.conf import settings
import bleach

def sanitize(value):
    return bleach.clean(
        value,
        tags=settings.BLEACH_ALLOWED_TAGS,
        attributes=settings.BLEACH_ALLOWED_ATTRIBUTES
    )
