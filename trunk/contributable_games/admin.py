from models import *
from django.contrib import admin

for a in Game, Profile, SavedPlay, LogEntry:
    admin.site.register(a)
    