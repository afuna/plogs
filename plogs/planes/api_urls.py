from rest_framework_extensions.routers import ExtendedDefaultRouter
from plogs.main.api_views import UserViewSet
from . import api_views as views

router = ExtendedDefaultRouter(trailing_slash=False)
(
    router.register(r'people', UserViewSet)
          .register(r'planes', views.UserPlaneViewSet,
                    base_name='user-planes',
                    parents_query_lookups=['owner__username']
                    )
)

urlpatterns = router.urls
