from django.db import models

class Research(models.Model):
    """Model for research"""
    




class Participant(models.Model):
    """Database model for Participant"""
    character_name = models.CharField(max_length=255, blank=True, null=True)
    daily_mission_score = models.PositiveIntegerField(blank=True, null=True)
    was_killer = models.BooleanField(default=False,blank=True, null=True)
    killer_round = models.SmallIntegerField(blank=True, null=True)
    votes = models.ForeignKey(
        'Vote',
        on_delete=models.CASCADE
    )
    game_appearance = models.OneToOneField(
        'research.GameAppearance',
        on_delete = models.CASCADE
    )

class GameAppearance(models.Model):
    """Database model for player appearance in game"""
    hair = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    items = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

class Vote(models.Model):
    nominee = models.CharField(max_length=255)
    round = models.SmallIntegerField()
    time_stamp = models.TimeField(auto_now_add=True)