from django_evolution.mutations import *
from django.db import models
from contributable_games.models import BigIntegerField

MUTATIONS = [
    DeleteField('GameResource', 'name'),
    DeleteField('GamePage', 'name'),
    AddField('LogEntry', 'order', BigIntegerField, initial=0),
    AddField('LogEntry', 'type', models.CharField, initial='legacy event', max_length=255)
]
