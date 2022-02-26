from rest_framework import serializers
from profiles import models

class GameAppearanceSerializer(serializers.ModelSerializer):
    """Serializer a game_appearance for participant"""
    class Meta:
        model = models.GameAppearance
        fields = ('hair', 'gender', 'items', 'color')

class UserProfileSerializer(serializers.ModelSerializer):
    "Serializers a user profile object"

    class Meta:
        model = models.UserProfile
        
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password'
        )
        
        extra_kwargs = {
            'password' : {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validation_data):
        """Create and return a new user"""

        user = models.UserProfile.objects.create_user(
            email=validation_data['email'],
            first_name=validation_data['first_name'],
            last_name=validation_data['last_name'],
            password=validation_data['password']
        )

        return  user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)

class ResearcherSerializer(UserProfileSerializer):
    """Serializer a Researcher object"""

    organization = serializers.CharField(max_length= 30)

    class Meta(UserProfileSerializer.Meta):
        fields = UserProfileSerializer.Meta.fields + ('organization',)

class ParticipantSerializer(UserProfileSerializer):
    """Serializer a Researcher object"""
    
    character_name = serializers.CharField(max_length=30)
    daily_mission_score = serializers.IntegerField()
    was_killer = serializers.BooleanField(default=False)
    killer_round = serializers.IntegerField()
    game_appearance = GameAppearanceSerializer()

    class Meta(UserProfileSerializer.Meta):
        fields = UserProfileSerializer.Meta.fields + (
            'character_name',
            'daily_mission_score',
            'was_killer',
            'killer_round',
            'game_appearance'
        )





