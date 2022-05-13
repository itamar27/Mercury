from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from research.models import (
    GameConfiguration,
    Participant,
    Interactions
)
from research.serializers import (
    GameConfigurationSerializer,
    InteractionSerializer,
    ParticipantSerializer,
) 
from django.http import Http404

import logging
logger = logging.getLogger(__name__)

class PlayerDetail(APIView):
    """
    Retrieve, update or delete a Participant instance.
    """
    serializer_class = ParticipantSerializer
    
    def get_object(self, pk):
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise Http404

    def get_player_with_email(self, email):
        try:
            return Participant.objects.get(email=email)
        except Participant.DoesNotExist:
            raise Http404

    def get(self, request):
        player_email = request.query_params.get('email', None)
        
        if player_email:
            participant = self.get_player_with_email(player_email)
        serializer = self.serializer_class(participant)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        participant = self.get_object(pk)
        serializer = self.serializer_class(participant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        Participant = self.get_object(pk)
        serializer = self.serializer_class(Participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Participant = self.get_object(pk)
        Participant.delete()

class GameConfigurationDetail(APIView):

    serializer_class = GameConfigurationSerializer

    def get_configuration_with_game_key(self, gc):
        try:
            return GameConfiguration.objects.get(game_code=gc)
        except Participant.DoesNotExist:
            raise Http404

    def get(self, request):
        configuration_id = request.query_params.get('configuration', None)
        
        if configuration_id:
            config = self.get_configuration_with_game_key(configuration_id)

        serializer = self.serializer_class(config)
        return Response(serializer.data)

class InteractionDetail(APIView):
    """Class to manage all project interactions"""
    serializer_class = InteractionSerializer
      
    def post(self, request):
        """Create a research interaction"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Creating new interaction - {serializer.data.get('id')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)