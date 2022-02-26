from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


from profiles.serializers import ResearcherSerializer, ParticipantSerializer
from profiles.models import Researcher, Participant
from profiles import permissions

import logging

logger = logging.getLogger(__name__)


class ResearcherListApiView(APIView):
    """API View class for a list of Researcher"""


    def get(self, request):
        """Returns a list of all researchers in the system"""

        logger.info("Getting All Researchers")
        
        objects = Researcher.objects.all()
        researchers = ResearcherSerializer(objects, many=True)

        return Response({"data": researchers.data})

class ResearcherDetailApiView(APIView):
    """API View class for single Researcher"""
  
    def get_object(self, pk):
        try:
            return Researcher.objects.get(pk=pk)
        except Researcher.DoesNotExist:
            raise Http404
  
    def get(self,request, pk):
        """Return a single Researcher"""

        logger.info('Getting a Researcher')

        try:        
            object = self.get_object(pk)
            researcher = ResearcherSerializer(object)
        except Http404:
            message = f"No matched data for {pk}"
            logger.error(message)
            logger.info(message)
            return Response({"data": message}, status= status.HTTP_400_BAD_REQUEST)
            

        return Response({"data":researcher.data}, status= status.HTTP_200_OK)


class ParticipantListApiView(APIView):
    """API View class for a list of Participant"""

    def get(self, request):
        """Returns a list of all Participants in the system"""

        logger.info("Getting All Participants")
        
        objects = Participant.objects.all()
        participants = ParticipantSerializer(objects, many=True)

        return Response({"data": participants.data})

class ParticipantDetailApiView(APIView):
    """API View class for single Researcher"""
  
    def get_object(self, pk):
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise Http404
  
    def get(self,request, pk):
        """Return a single Participant"""

        logger.info('Getting a Participant')

        try:        
            object = self.get_object(pk)
            participant = ParticipantSerializer(object)
        except Http404:
            message = f"No matched data for {pk}"
            logger.error(message)
            return Response({"data": message}, status= status.HTTP_400_BAD_REQUEST)
            

        return Response({"data":participant.data}, status= status.HTTP_200_OK)