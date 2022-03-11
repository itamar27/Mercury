from django.contrib import admin
from research import models

admin.site.register(models.Research)
admin.site.register(models.Participant)
admin.site.register(models.GameAppearance)
admin.site.register(models.Interactions, models.StatAdmin)