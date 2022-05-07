import uuid
from django.db import models
from django.contrib import admin

class Research(models.Model):
    """Model for research"""
    pass

class GameConfiguration(models.Model):
    """Database model for game configuration json data"""
    OPTIMAL = 1
    SUB_OPTIMAL = 2
    BOOT_STRATEGY_CHOICE = [
        (OPTIMAL, 'Optimal'),
        (SUB_OPTIMAL, 'SubOptimal')
    ]

    game_code = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    start_time = models.DateTimeField()
    agents_behaviors = models.CharField(
        max_length= 50,
        choices=BOOT_STRATEGY_CHOICE,
        default=OPTIMAL
    )

    def __str__(self):
        return str(self.game_code)
        
class Participant(models.Model):
    """Database model for Participant"""
    email = models.EmailField(unique=True)
    character_name = models.CharField(max_length=255, blank=True, null=True)
    daily_mission_score = models.PositiveIntegerField(blank=True, null=True)
    was_killer = models.BooleanField(default=False,blank=True, null=True)
    killer_round = models.SmallIntegerField(default= -1, blank=True, null=True)
    
    votes = models.ForeignKey(
        'research.Vote',
        on_delete=models.CASCADE, 
        blank=True,
        null=True
    )

    game_appearance = models.OneToOneField(
        'research.GameAppearance',
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.email

class GameAppearance(models.Model):
    """Database model for player appearance in game"""
    hair = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    items = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"hair {self.hair}, color {self.color},gender {self.gender},items {self.items}"

class Vote(models.Model):
    nominee = models.CharField(max_length=255, blank=True, null=True)
    round = models.SmallIntegerField(blank=True, null=True)
    time_stamp = models.TimeField(auto_now_add=True)


class Interactions(models.Model):
    """Datebase model for interaction of two players in game"""
    source = models.CharField(max_length=5)
    target = models.CharField(max_length=5)
    score = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    round = models.SmallIntegerField(blank=True, null=True)
    time_stamp = models.TimeField(auto_now_add=True)

def download_csv(modeladmin, request, queryset):
    import csv
    f = open('some.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(["source", "target", "message", "time_stamp"])
    for s in queryset:
        writer.writerow([s.source, s.target, s.message, s.time_stamp])

class StatAdmin(admin.ModelAdmin):
    list_display = ('source', 'target', 'message', 'time_stamp')
    actions = [download_csv]

class Clues(models.Model):
    """Database model to represent all clues and their"""
    #TBD after alpha phase
    pass


