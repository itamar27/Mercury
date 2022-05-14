from rest_framework import serializers
from research.models import (
    Research, Participant, GameConfiguration, 
    GameAppearance, Vote, Interactions
)

class GameConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameConfiguration
        fields = '__all__' 

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interactions
        fields = '__all__'

class GameAppearanceSerializer(serializers.ModelSerializer):
    """Serializer for game appearance models"""

    class Meta:
        model = GameAppearance
        fields = ['id', 'hair', 'color','items', 'gender']

            
class VotesSerializer(serializers.ModelSerializer):
    """Serializer for game appearance models"""

    class Meta:
        model = Vote
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    """Serializes for participant model"""
    email = serializers.EmailField()
    character_name = serializers.CharField(max_length=25, required=False)
    daily_mission_score = serializers.IntegerField(required=False)
    was_killer = serializers.BooleanField(required=False)
    killer_round = serializers.IntegerField(required=False)
    votes = VotesSerializer(required=False, many=True)
    game_appearance = GameAppearanceSerializer(required=False)
    
    class Meta:
        model = Participant
        fields = ['id','email', 'character_name', 'daily_mission_score', 'was_killer', 'killer_round', 'votes', 'game_appearance']
        depth = 1

    def create(self, validated_data):
        """Override default create method for inner models instance"""
        participant = Participant.objects.create(**validated_data)
        return participant

    def update(self, instance,validated_data):
        """Update a participant"""
        game_appearance_data = validated_data.pop('game_appearance', None)
        vote_data = validated_data.pop('votes', None)
        if game_appearance_data:
            game_appearance = GameAppearance(participant = instance,**game_appearance_data)
            game_appearance.save()
        if vote_data:
            vote = Vote(**vote_data)
            vote.save()
        instance.email = validated_data.pop('email', instance.email)
        instance.character_name = validated_data.pop('character_name', instance.character_name)
        instance.daily_mission_score = validated_data.pop('daily_mission_score', instance.daily_mission_score)
        instance.was_killer = validated_data.pop('was_killer', instance.was_killer)
        instance.killer_round = validated_data.pop('killer_round', instance.killer_round)

        instance.save()

        return instance

class ResearchSerializer(serializers.ModelSerializer):
    """Serializes for participant model"""
    research_name = serializers.CharField(max_length=24, default="")
    research_description = serializers.CharField(max_length=150, default="")
    game_configuration = GameConfigurationSerializer(required=False, default = None)
    participants = ParticipantSerializer(many=True)
    interactions = InteractionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Research
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        """Override default create method for inner models instance"""
        game_configuration = validated_data.pop('game_configuration')
        participants = validated_data.pop('participants')
        research = Research.objects.create(**validated_data)
        GameConfiguration.objects.create(research=research, **game_configuration)
        
        for participant in participants:
            Participant.objects.create(research=research, **participant)

        return research