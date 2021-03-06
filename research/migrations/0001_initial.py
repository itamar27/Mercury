# Generated by Django 4.0.3 on 2022-05-21 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('character_name', models.CharField(blank=True, max_length=255, null=True)),
                ('daily_mission_score', models.PositiveIntegerField(blank=True, null=True)),
                ('was_killer', models.BooleanField(blank=True, default=False, null=True)),
                ('killer_round', models.SmallIntegerField(blank=True, default=-1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominee', models.CharField(blank=True, max_length=255, null=True)),
                ('round', models.SmallIntegerField(blank=True, null=True)),
                ('time_stamp', models.TimeField(auto_now_add=True)),
                ('participant_vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='research.participant')),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('research_name', models.CharField(default='', max_length=24)),
                ('research_description', models.TextField(default=None, max_length=150, null=True)),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='researchs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='research',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='research.research'),
        ),
        migrations.CreateModel(
            name='Interactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=10)),
                ('target', models.CharField(max_length=10)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('round', models.SmallIntegerField(blank=True, null=True)),
                ('time_stamp', models.TimeField(auto_now_add=True)),
                ('research', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='research.research')),
            ],
        ),
        migrations.CreateModel(
            name='GameConfiguration',
            fields=[
                ('game_code', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=5, max_length=5, prefix='', primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('agents_behaviors', models.CharField(choices=[(1, 'Optimal'), (2, 'SubOptimal')], default=1, max_length=50)),
                ('research', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_configuration', to='research.research')),
            ],
        ),
        migrations.CreateModel(
            name='GameAppearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hair', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('items', models.CharField(blank=True, max_length=20, null=True)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('participant', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_appearance', to='research.participant')),
            ],
        ),
        migrations.CreateModel(
            name='Clue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=256)),
                ('round', models.SmallIntegerField(blank=True, null=True)),
                ('type', models.CharField(choices=[(1, 'common'), (2, 'hidden')], default=None, max_length=50, null=True)),
                ('participant', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clue', to='research.participant')),
                ('research', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clue', to='research.research')),
            ],
        ),
    ]
