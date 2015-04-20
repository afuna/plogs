from rest_framework import viewsets, permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.contrib.auth.models import User
from . import serializers

class UserViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class AuthenticatedCheckView(APIView):
	"""
	Checks whether the user is authenticated or not
	(a bit simple; signin is not done over API yet)
	"""
	permission_classes = (permissions.AllowAny,)

	def get(self, request, format=None):
		if request.user.is_authenticated():
			content = {
				"user": unicode(request.user.username),
				"authenticated": True
			}
		else:
			content = {
				"authenticated": False
			}

		return Response(content)