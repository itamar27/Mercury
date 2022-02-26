# Generated by Django 4.0.2 on 2022-02-21 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameAppearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hair', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('items', models.CharField(blank=True, max_length=20, null=True)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('userprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('profiles.userprofile',),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('userprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('character_name', models.CharField(blank=True, max_length=255, null=True)),
                ('daily_mission_score', models.PositiveIntegerField(blank=True, null=True)),
                ('was_killer', models.BooleanField(blank=True, default=False, null=True)),
                ('killer_round', models.SmallIntegerField(blank=True, null=True)),
                ('game_appearance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.gameappearance')),
            ],
            options={
                'abstract': False,
            },
            bases=('profiles.userprofile',),
        ),
    ]