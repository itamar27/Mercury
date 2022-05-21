import uuid
from django.db import models
from django.contrib import admin
from shortuuid.django_fields import ShortUUIDField



class Research(models.Model):
    """Model for research"""
    research_name = models.CharField(max_length=24, default="")
    research_description = models.TextField(max_length=150, null=True ,default=None)
    
    researcher = models.ForeignKey(
        'profiles.Researcher',
        on_delete=models.CASCADE,
        related_name='researchs',
    )


class GameConfiguration(models.Model):
    """Database model for game configuration json data"""
    OPTIMAL = 1
    SUB_OPTIMAL = 2
    BOOT_STRATEGY_CHOICE = [
        (OPTIMAL, 'Optimal'),
        (SUB_OPTIMAL, 'SubOptimal')
    ]

    game_code = ShortUUIDField(primary_key=True, length=5 ,editable=False)
    start_time = models.DateTimeField()
    agents_behaviors = models.CharField(
        max_length=50,
        choices=BOOT_STRATEGY_CHOICE,
        default=OPTIMAL
    )
    
    research = models.OneToOneField(
        'research.Research',
        on_delete=models.CASCADE,
        related_name='game_configuration',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.game_code)


class Participant(models.Model):
    """Database model for Participant"""
    email = models.EmailField(unique=True)
    character_name = models.CharField(max_length=255, blank=True, null=True)
    daily_mission_score = models.PositiveIntegerField(blank=True, null=True)
    was_killer = models.BooleanField(default=False, blank=True, null=True)
    killer_round = models.SmallIntegerField(default=-1, blank=True, null=True)

    research = models.ForeignKey(
        'research.Research',
        on_delete=models.CASCADE,
        related_name='participants',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.email

class GameAppearance(models.Model):
    """Database model for player appearance in game"""
    hair = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    items = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    participant = models.OneToOneField(
        'research.Participant',
        on_delete=models.CASCADE,
        related_name = 'game_appearance',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"hair {self.hair}, color {self.color},gender {self.gender},items {self.items}"


class Vote(models.Model):
    nominee = models.CharField(max_length=255, blank=True, null=True)
    round = models.SmallIntegerField(blank=True, null=True)
    time_stamp = models.TimeField(auto_now_add=True)
    participant_vote = models.ForeignKey(
        'research.Participant',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class Interactions(models.Model):
    """Datebase model for interaction of two players in game"""
    source = models.CharField(max_length=10)
    target = models.CharField(max_length=10)
    score = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    round = models.SmallIntegerField(blank=True, null=True)
    time_stamp = models.TimeField(auto_now_add=True)

    research = models.ForeignKey(
        'research.Research',
        on_delete=models.CASCADE,
        related_name = 'interactions',
        blank=True,
        null=True
    )


class Clue(models.Model):
    """Database model ton represent all clues and their"""
    COMMON = 1
    HIDDEN = 2
    CLUE_TYPE_CHOICE = [
        (COMMON, 'common'),
        (HIDDEN, 'hidden')
    ]
    
    message = models.CharField(max_length = 256)
    round = models.SmallIntegerField(blank=True, null=True)
    type = models.CharField(
        max_length=50,
        choices=CLUE_TYPE_CHOICE,
        null=True,
        default=None
    )

    participant = models.ForeignKey(
        'research.Participant',
        on_delete=models.CASCADE,
        related_name='clue',
        null=True
    )

    research = models.ForeignKey(
        'research.Research',
        on_delete=models.CASCADE,
        related_name='clue',
        null=True
    )
    
    