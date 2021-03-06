from plogs.main.api_views import UserViewSet
from plogs.main.routers import NestedDefaultRouter
from . import api_views as views


root_router = NestedDefaultRouter(trailing_slash=False)

people_router = root_router.register(r'people', UserViewSet)

projects_router = people_router.register(r'projects',
                        views.ProjectViewSet,
                        base_name='user-projects',
                        parents_query_lookups=['user__username'])

buildlogs_router = projects_router.register(
                        r'buildlogs',
                        views.BuildLogViewSet,
                        base_name='project-buildlogs',
                        parents_query_lookups=['project__user__username', 'project__slug'])

buildlogs_router.register(r'images',
                          views.BuildLogImageViewSet,
                          base_name='buildlog-images',
                          parents_query_lookups=['build__project__user__username',
                                                 'build__project__slug', 'build__log_id'])

people_router.register(r'categories',
                       views.CategoryViewSet,
                       base_name='user-categories',
                       parents_query_lookups=['user__username'])

people_router.register(r'partners',
                       views.PartnerViewSet,
                       base_name='user-partners',
                       parents_query_lookups=['user__username'])

root_router.register(r'projects/active', views.ActiveProjectViewSet, base_name='project-active')

urlpatterns = root_router.urls
