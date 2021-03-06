from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.shortcuts import render

import os

import network.network_utils  as Network 
from research.models import Participant, Interactions, GameConfiguration, Research
from research.serializers import (
    ParticipantSerializer,
    InteractionSerializer, 
    GameConfigurationSerializer,
    ResearchSerializer
)
import logging

logger = logging.getLogger(__name__)

class ResearchApiViewList(APIView):

    serializer_class = ResearchSerializer
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        """Research details that belongs to the researcher"""
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)
        research = Research.objects.all()
        serializer = self.serializer_class(research, many=True)
        response_status = status.HTTP_200_OK
        return  Response({"data": serializer.data}, status = response_status)
    
    def post(self, request):
        """Create a new research object"""
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Research created successfully",
            }
            ## TBD - send emails to participants once research is created!
            return Response(response, status=status.HTTP_201_CREATED)
        logger.error(f'\n\n{serializer.errors}\n')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchApiViewDetail(APIView):

    serializer_class = ResearchSerializer
    permissions_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Research.objects.get(pk=pk)
        except Research.DoesNotExist:
            raise Http404

    def get(self, request, researchId):
        """Return Research detail for requested research"""

        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)
        research = self.get_object(pk =researchId)
        serializer = self.serializer_class(research)
        data = serializer.data
        data.update({'interactions': len(data.get('interactions'))})
        response_status = status.HTTP_200_OK
        return  Response({"data": data}, status = response_status)

    
    def delete(self, request, pk, format=None):

        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)
        
        research = self.get_object(pk)
        research.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ParticipantList(APIView):
    """A view class to manage participants"""
    serializer_class = ParticipantSerializer
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        """Return list of participants"""

        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        participants = Participant.objects.all()
        serializer = self.serializer_class(participants, many=True)
        response_status = status.HTTP_200_OK
        return  Response({"data": serializer.data}, status = response_status)
    
    def post(self, request):
        """Create a new Participant"""
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

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
    
    def get_object(self, pk):
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        participant = self.get_object(pk)
        serializer = self.serializer_class(participant)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        participant = self.get_object(pk)
        serializer = self.serializer_class(participant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        Participant = self.get_object(pk)
        serializer = self.serializer_class(Participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        
        if not request.user.is_authenticated:
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        Participant = self.get_object(pk)
        Participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NetworkAPIView(APIView):
    """Class to manage network view"""
    serializer_class = ResearchSerializer
    permissions_classes = [IsAuthenticated]

    
    def get(self, request, researchId):
        """Return Research detail for requested research"""

        if not request.user.is_authenticated:
            logger.error("User is not authenticated")
            return  Response({"error": "User is not authenticated"}, status = status.HTTP_400_BAD_REQUEST)

        round = request.query_params.get('round', None)
        error = None
        centrality = None
        density = None
        diameter = None
        reciprocity = None
        radius = None

        directed = request.query_params.get('directed', True) 
        research = Research.objects.get(id =researchId)
        serializer = self.serializer_class(research)
        interactions =serializer.data.get('interactions') 


        if round:
            tmp = []
            for interaction in interactions:
                if interaction['round'] == int(round):
                    tmp.append(interaction)
            interactions = tmp

        """Get list of research interactions"""
        response_status = status.HTTP_200_OK
        logger.info("Creating a network from all interaction for current research")
        
        network = Network.create_network(interactions, directed=directed)
        edges = list(network.edges(data=True))
        nodes = list(network.nodes)

        if request.query_params.get('centrality', None) and network:
            try:
                centrality = Network.calculate_betweens(network)
            except Network.nx.NetworkXException as e:
                logger.error(f'Could not calculate betweens for network\n{e}')
                error = str(e)

        if request.query_params.get('density', None) and network:
            try:
                density = Network.calculate_density(network)
            except Network.nx.NetworkXException as e:
                logger.error(f'Could not calculate density for network\n{e}')
                error = str(e)

        if request.query_params.get('radius', None) and network:
            try:
                radius = Network.calculate_radius(network)
            except Network.nx.NetworkXException as e:
                logger.error(f'Could not calculate radius for network\n{e}')
                error = str(e)

        if request.query_params.get('diameter', None) and network:
            try:
                diameter = Network.calculate_diameter(network)
            except Network.nx.NetworkXException as e:
                logger.error(f'Could not calculate diameter for network\n{e}')
                error = str(e)

        if request.query_params.get('reciprocity', None) and network:
            try:
                reciprocity = Network.calculate_reciprocity(network)
            except Network.nx.NetworkXException as e:
                logger.error(f'Could not calculate reciprocity for network\n{e}')
                error = str(e)

        response = {
            'graph': {
                'nodes': nodes,
                'edges': edges,
            },
            'node_count': len(nodes),
            'edges_count': len(edges),
            'diameter': diameter,
            'radius': radius,
            'centrality': centrality,
            'reciprocity': reciprocity,
            'density': density,
            'error': error,
        }

        return Response(response, status=response_status)
