from plogs.main.api_views import UserViewSet
from plogs.main.routers import NestedDefaultRouter
from . import api_views as views

router = NestedDefaultRouter(trailing_slash=False)
(
    router.register(r'people', UserViewSet)
          .register(r'planes', views.UserPlaneViewSet,
                    base_name='user-planes',
                    parents_query_lookups=['owner__username']
                    )
)

urlpatterns = router.urls
