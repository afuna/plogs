from rest_framework_extensions.routers import ExtendedDefaultRouter
from plogs.main.api_views import UserViewSet
from . import api_views as views

router = ExtendedDefaultRouter(trailing_slash=False)

people_router = router.register(r'people', UserViewSet)

projects_router = people_router.register(r'projects',
                        views.ProjectViewSet,
                        base_name='user-projects',
                        parents_query_lookups=['plane__owner__username'])

buildlogs_router = projects_router.register(
                        r'buildlogs',
                        views.BuildLogViewSet,
                        base_name='project-buildlogs',
                        parents_query_lookups=['project__plane__owner__username', 'project__id'])


urlpatterns = router.urls
