# Generated by Django 4.0.3 on 2022-05-13 10:20

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0009_alter_research_research_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=5, max_length=5, prefix='', primary_key=True, serialize=False),
        ),
    ]
