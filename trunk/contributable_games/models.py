from django.db import models
from django.contrib.auth.models import User
from django.utils.simplejson import dumps, loads
from django.core.urlresolvers import reverse
from django.conf import settings
import os
from os import path

class BigIntegerField(models.IntegerField):
    def db_type(self):
        return 'bigint'

class Profile(User):
    can_upload_games = models.BooleanField(default=False)
    birthdate = models.DateField()
    gender = models.SmallIntegerField(choices=[(1,'male'),(2,'female')])
    handedness = models.SmallIntegerField(choices=[(1,'right'),(2,'left'),(3,'both')],default=1)
    siblingnumber = models.PositiveIntegerField(default=0);
    avatar = models.ImageField(upload_to='avatares',default='avatares/pepe.gif',height_field='80px',width_field='80px');
    
class Game(models.Model):
    name = models.SlugField(max_length=200, unique=True)
    profile = models.ForeignKey(Profile)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField(default='No hay')
    
    @property
    def static_dir(self):
        return 'games/%s' % self.name
    @property
    def abspath(self):
        return path.join(settings.MEDIA_ROOT, self.static_dir)
    
    @property
    def resource_path(self):
        return "%s/res/" % self.static_dir
    @property
    def page_path(self):
        return "%s/pages/" % self.static_dir
    @property
    def abs_pages_path(self):
        return path.join(settings.MEDIA_ROOT, self.page_path)
    @property
    def game_file_path(self):
        return "%s/game_files/" % self.static_dir
    @property
    def screenshots_path(self):
        return "%s/screenshots/" % self.static_dir
    @property
    def abs_screenshots_path(self):
        return path.join(settings.MEDIA_ROOT, self.screenshots_path)

    def __unicode__(self):
        return self.title
    
    @property
    def view_game_url(self):
        return settings.GAMES_SITE_DOMAIN +self.name
                
                
    @property
    def login_url(self):
        return settings.MAIN_SITE_DOMAIN + \
                reverse('login_to_game', args=[self.name], urlconf="urls_main_site")
    
    def _flatten_walk(self, subdir, include_dirs = False):
        '''Returns a flat list of file paths for all files in the given subdir, all relative to subdir'''
        paths = []
        for dirpath, dirnames, filenames in os.walk(path.join(settings.MEDIA_ROOT, subdir)):
            if '/.' in dirpath: continue
            curdir = dirpath[len(self.abspath)+1:]
            if include_dirs and curdir:
                paths.append(curdir)
            paths += [path.join(curdir,f) for f in filenames if not f.startswith('.')]
        return paths
    
    @property
    def files(self):
        '''All files related to this game'''
        return self._flatten_walk(self.static_dir)
    
    @property
    def files_and_dirs(self):
        return self._flatten_walk(self.static_dir, True)
        
    @property
    def game_files(self):
        '''All game_files related to this game'''
        return self._flatten_walk(self.game_file_path)
    
    @property
    def image_url(self):
        try:
            screenshots = [x for x in os.listdir(self.abs_screenshots_path)
                                if x[-4:].lower() in ('.png', '.gif','.jpg')]
        except OSError:
            return ''
        
        if screenshots:
            return path.join(settings.MEDIA_URL, self.screenshots_path, screenshots[0])
        return ''
    
    
    @property
    def ranking(self):
        ranking = SavedPlay.objects.filter(game=self).order_by('-score')
        checked = []
        rankingU=[]
        p = 0;
        try:
            for e in ranking:
                if e.profile not in checked:
                    checked.append(e.profile)
                    p = p + 1;
                    rankingU.append({'profile': e.profile, 'score': e.score, 'puesto': p})
               
        except(AttributeError):
            print "a"
            
        return rankingU
        
    def create_directory_structure(self):
        for dirname in self.resource_path, self.page_path, self.game_file_path, self.screenshots_path:
            d = os.path.join(settings.MEDIA_ROOT, dirname)
            if not os.path.exists(d): os.makedirs(d)

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
    
