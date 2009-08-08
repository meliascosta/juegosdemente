from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    AddField('GameResource', 'name', models.CharField, initial='some_file', max_length=200),
    AddField('GamePage', 'name', models.CharField, initial='some_file', max_length=200)
]
