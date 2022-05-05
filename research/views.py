from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import render

import os

from network.network_utils import create_network
from research.models import Participant, Interactions, GameConfiguration
from research.serializers import ParticipantSerializer,InteractionSerializer, GameConfigurationSerializer

import logging

logger = logging.getLogger(__name__)

class ParticipantList(APIView):
    """A view class to manage participants"""
    serializer_class = ParticipantSerializer
    
    def get(self, request):
        """Return list of participants"""        
        participants = Participant.objects.all()
        serializer = self.serializer_class(participants, many=True)
        response_status = status.HTTP_200_OK
        return  Response({"data": serializer.data}, status = response_status)
    
    def post(self, request):
        """Create a new Participant"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

           
class ParticipantDetails(APIView):
    """
    Retrieve, update or delete a Participant instance.
    """
    serializer_class = ParticipantSerializer
    
    def get_object(self, pk, researchId):
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise Http404

    def get(self, request, pk, researchId, format=None):
        participant = self.get_object(pk)
        serializer = self.serializer_class(participant)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        Participant = self.get_object(pk)
        serializer = self.serializer_class(Participant, data=request.data, partial=True)
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
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class InteractionList(APIView):
    """Class to manage all project interactions"""
    serializer_class = InteractionSerializer
    
    def get(self, request):
        """Get list of research interactions"""
        
        interactions = Interactions.objects.all()
        serializer = self.serializer_class(interactions, many=True)
        response_status = status.HTTP_200_OK

        logger.info("Retrieving all interaction for current research")
        return  Response({"data": serializer.data}, status = response_status)
    
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


class InteractionsNetworkAPIView(APIView):
    """Class to manage network view"""
    serializer_class = InteractionSerializer
    
    def get(self, request):
        """Get list of research interactions"""
        
        interactions = Interactions.objects.all()
        serializer = self.serializer_class(interactions, many=True)
        response_status = status.HTTP_200_OK
        create_network(serializer.data)
        path = os.path.join(os.getcwd(),'research/templates/Interactions/interactions.html')
        print(f'\n\n{os.path.exists(path)}')
        logger.info("Creating a network from all interaction for current research")
        return render(request, path, status=response_status)


class GameConfigurationDetail(APIView):
    """Class to manage research configuration"""
    
    serializer_class = GameConfigurationSerializer
    
    def get_object(self, pk):
        try:
            return GameConfiguration.objects.get(pk=pk)
        except GameConfiguration.DoesNotExist:
            raise Http404

    def get(self, request, researchId, format=None):
        gameconfig = self.get_object(researchId)
        serializer = self.serializer_class(gameconfig)
        return Response(serializer.data)
    
    def post(self, researchId,request):
        """Create a research game configuration"""
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Creating new interaction - {serializer.data.get('game_code')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)