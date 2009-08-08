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
    image = models.ImageField(upload_to = lambda s,i: "%s/main_image/%s" % (s.static_dir,i))
    
    @property
    def static_dir(self):
        return 'games/%s' % self.name
    
    @property
    def resource_path(self):
        return "%s/res/" % self.static_dir
    
    @property
    def page_path(self):
        return "%s/pages/" % self.static_dir
    
    
class _GameRes(models.Model):
    class Meta:
        abstract = True

    game = models.ForeignKey(Game)
    
    def delete(self):
        self.file.delete()
        return super(_GameRes, self).delete()
    
    def __unicode__(self):
        return unicode(self.file.name)
    
class GameResource(_GameRes):
    file = models.FileField(upload_to = lambda s,i: s.game.resource_path+i)
    
class GamePage(_GameRes):
    file = models.FileField(upload_to = lambda s,i: s.game.page_path+i)

class SavedPlay(models.Model):
    game = models.ForeignKey(Game)
    profile = models.ForeignKey(Profile, null=True)
    ip = models.IPAddressField()
    score = models.IntegerField()
    
class LogEntry(models.Model):
    savedplay = models.ForeignKey(SavedPlay)
    ms = BigIntegerField()
    type = models.CharField(max_length=255)
    order = BigIntegerField()
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
    file = models.FileField(upload_to = lambda s,i: "%s/game_files/%s" % (s.game.static_dir, i))
    
