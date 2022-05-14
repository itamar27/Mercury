from rest_framework import serializers
from profiles import models
from research.serializers import ResearchSerializer

class ResearcherSerializer(serializers.ModelSerializer):
    "Serializers a researcher object"
    researchs = ResearchSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Researcher
        fields = ['id', 'first_name', 'last_name', 'password','email','researchs']

        extra_kwargs = {
            'password' : {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validation_data):
        """Create and return a new user"""
        user = models.Researcher.objects.create_user(
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









