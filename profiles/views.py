import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions


from profiles.serializers import ResearcherSerializer
from profiles.models import Researcher
from research.models import Research
from profiles import permissions as my_permissions
from django.http import Http404


import logging
logger = logging.getLogger(__name__)

class ResearcherViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = ResearcherSerializer
    queryset = Researcher.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (my_permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name','last_name', 'email')


class ResearcherDetails(APIView):
    serializer_class = ResearcherSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Researcher.objects.get(pk=pk)
        except Researcher.DoesNotExist:
            raise Http404

    def get(self, request, pk):

        researcher = self.get_object(pk)
        if researcher.email == request.user.email:
            serializer = self.serializer_class(researcher)
            researches = serializer.data.get('researchs')
            researches_data = []
            res = {
                'email': serializer.data.get('email'),
                'first_name': serializer.data.get('first_name'),
                'id': serializer.data.get('id'), 
            }
            for research in researches:
                researches_data.append({
                    'research_name': research.get('research_name'),
                    'research_description': research.get('research_description'),
                    'participants': len(research.get('participants')),
                    'start_time': research.get('game_configuration').get('start_time'),
                    'research_id': research.get('id')

                })
            res['researches'] = researches_data
            return Response(res)
        else:
            return Response({'error':'You are not permittied to view this data'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        #Check if user is already authenticated
        logger.info("Trying to authenticated user")
        if request.user.is_authenticated:
            return Response({
                'id': request.user.id,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            },status=status.HTTP_200_OK)

        password = request.data.get('password')
        try:
            user = Researcher.objects.get(email=request.data.get('username'))
        except Researcher.DoesNotExist as e:
           return Response({'error': "Researcher email is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({'error': "Researcher password is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user= user)
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token.key
        },status=status.HTTP_200_OK)