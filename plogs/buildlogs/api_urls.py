from plogs.main.api_views import UserViewSet
from plogs.main.routers import NestedDefaultRouter
from . import api_views as views


root_router = NestedDefaultRouter(trailing_slash=False)

people_router = root_router.register(r'people', UserViewSet)

projects_router = people_router.register(r'projects',
                        views.ProjectViewSet,
                        base_name='user-projects',
                        parents_query_lookups=['plane__owner__username'])

buildlogs_router = projects_router.register(
                        r'buildlogs',
                        views.BuildLogViewSet,
                        base_name='project-buildlogs',
                        parents_query_lookups=['project__plane__owner__username', 'project__id'])

root_router.register(r'projects/active', views.ActiveProjectViewSet, base_name='project-active')

urlpatterns = root_router.urls
