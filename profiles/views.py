import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from profiles.serializers import ResearcherSerializer
from profiles.models import Researcher
from profiles import permissions

import logging

logger = logging.getLogger(__name__)


class ResearcherViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = ResearcherSerializer
    queryset = Researcher.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name','last_name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):

        password = request.data.get('password')
        try:
            user = Researcher.objects.get(email=request.data.get('username'))
        except Researcher.DoesNotExist as e:
           return Response({'error': "Researcher email is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({'error': "Researcher password is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        print(user.id)
        token, created = Token.objects.get_or_create(user= user)
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token.key
        },status=status.HTTP_200_OK)
