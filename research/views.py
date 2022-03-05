from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from research.models import Participant
from research.serializers import ParticipantSerializer


class ParticipantList(APIView):
    """A view class to manage participants"""

    def get(self, request):
        """Return list of participants"""        
        
        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)
        response_status = status.HTTP_200_OK
        return  Response({"data": serializer.data}, status = response_status)
    
    def post(self, requst):
        """Create a new Participant"""
    

class ParticipantDetails(APIView):
    """A view class to manage single Participant"""

    def get(self, request):
        """Return a single participant object"""
        pass
    
    def put(self, request):
        """Update a single object participant"""
        pass

    def patch(self, request):
        """Update a single field of participant"""
        pass
    
