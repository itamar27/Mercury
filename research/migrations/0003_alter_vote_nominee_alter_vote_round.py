# Generated by Django 4.0.2 on 2022-03-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0002_alter_participant_game_appearance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='nominee',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='round',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
