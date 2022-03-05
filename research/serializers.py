from rest_framework import serializers
from research.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializes for participant model"""

    class Meta:
        model = Participant
        fields = '__all__'
