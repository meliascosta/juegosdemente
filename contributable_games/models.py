from django.db import models
from django.contrib.auth.models import User
from django.utils.simplejson import dumps, loads

class BigIntegerField(models.IntegerField):
    def db_type(self):
        return 'bigint'

class Profile(User):
    can_upload_games = models.BooleanField(default=False)
    birthdate = models.DateField()
    gender = models.SmallIntegerField(choices=[(1,'male'),(2,'female')])
    
class Game(models.Model):
    name = models.SlugField(max_length=200, unique=True)
    profile = models.ForeignKey(Profile)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to = lambda s,i: "%s/main_image/" % s.static_dir)
    
    @property
    def static_dir(self):
        return 'games/%s' % self.name
    
class GameResource(models.Model):
    game = models.ForeignKey(Game)
    file = models.FileField(upload_to = lambda s,i: "%s/resources/" % s.game.static_dir)
    
class SavedPlay(models.Model):
    game = models.ForeignKey(Game)
    profile = models.ForeignKey(Profile, null=True)
    ip = models.IPAddressField()
    score = models.IntegerField()
    
class LogEntry(models.Model):
    savedplay = models.ForeignKey(SavedPlay)
    ms = BigIntegerField()
    _data = models.TextField()
    
    def _get_data(self):
        return loads(self._data)
    def _set_data(self, data):
        self._data = dumps(data) 
    data = property(_get_data, _set_data)
    
class GameFile(models.Model):
    game = models.ForeignKey(Game)
    nivel = models.IntegerField()
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to = lambda s,i: "%s/game_files/" % s.game.static_dir)
    
