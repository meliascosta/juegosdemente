from models import *
from django.contrib import admin

for a in Game, GameFile, GamePage, GameResource, Profile, SavedPlay, LogEntry:
    admin.site.register(a)
    