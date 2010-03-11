from django.db import models
from django.contrib.auth.models import User
from django.utils.simplejson import dumps, loads
from django.core.urlresolvers import reverse
from django.conf import settings
import os
from PIL import Image
from os import path

class BigIntegerField(models.IntegerField):
    def db_type(self):
        return 'bigint'

class Profile(User):
    can_upload_games = models.BooleanField(default=False)
    birthdate = models.DateField("Fecha de nacimiento")
    gender = models.SmallIntegerField("Sexo",choices=[(1,'hombre'),(2,'mujer')])
    handedness = models.SmallIntegerField("Mano mas habil",choices=[(1,'derecha'),(2,'izquierda'),(3,'ambas')])
    siblingnumber = models.PositiveIntegerField("Hermanos en total",default=0);
    siblingorder = models.PositiveIntegerField("Tu orden de hermandad (1 es el mas grande)",default=0);
    avatar = models.ImageField("tu avatar",upload_to='avatares',default='avatares/pepe.gif');
    is_school_player = models.BooleanField(default=False)
    school_games  = models.TextField("Lista de Juegos para Escuela",default="[\"planning\",\"planning\",\"planning\",\"planning\",\"planning\",\"planning\",\"planning\",\"planning\",\"control\",\"control\",\"control\",\"control\",\"control\",\"control\",\"control\",\"control\",\"memory\",\"memory\",\"memory\",\"memory\",\"memory\",\"memory\",\"memory\",\"memory\"]")
    current_school_game = models.PositiveIntegerField(default=0); #que le toca hoy
    current_state = models.TextField("Estado",default="{}")
    last_session_date = models.DateField(default='1981-10-14')
    def save(self, size=(100, 100)):
        """
            REQUIRES:
                1.    'from PIL import Image'
            
            DOES:
                1.    check to see if the image needs to be resized
                2.    check how to resize the image based on its aspect ratio
                3.    resize the image accordingly
            
            ABOUT:
                based loosely on djangosnippet #688
                http://www.djangosnippets.org/snippets/688/
            
            VERSIONS I'M WORKING WITH:
                Django 1.0
                Python 2.5.1
            
            BY:
                Tanner Netterville
                tanner@cabedge.com
        """
        
        if not self.id and not self.avatar:
            return
        
        super(Profile, self).save()
        
        pw = self.avatar.width
        ph = self.avatar.height
        nw = size[0]
        nh = size[1]
        
        # only do this if the image needs resizing
        if (pw, ph) != (nw, nh):
            filename = str(self.avatar.path)
            image = Image.open(filename)
            pr = float(pw) / float(ph)
            nr = float(nw) / float(nh)
            
            if pr > nr:
                # photo aspect is wider than destination ratio
                tw = int(round(nh * pr))
                image = image.resize((tw, nh), Image.ANTIALIAS)
                l = int(round(( tw - nw ) / 2.0))
                image = image.crop((l, 0, l + nw, nh))
            elif pr < nr:
                # photo aspect is taller than destination ratio
                th = int(round(nw / pr))
                image = image.resize((nw, th), Image.ANTIALIAS)
                t = int(round(( th - nh ) / 2.0))
                print((0, t, nw, t + nh))
                image = image.crop((0, t, nw, t + nh))
            else:
                # photo aspect matches the destination ratio
                image = image.resize(size, Image.ANTIALIAS)
                
            image.save(filename)

    
class Game(models.Model):
    name = models.SlugField(max_length=200, unique=True)
    profile = models.ForeignKey(Profile)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    school_max_time = models.PositiveIntegerField(default=1200);
    description = models.TextField(default='No hay')
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
        for e in ranking:
            try:
                if e.profile not in checked and e.profile is not None:
                    #import pdb
                    #pdb.set_trace()
                    checked.append(e.profile)
                    p = p + 1;
                    rankingU.append({'profile': e.profile, 'score': e.score, 'puesto': p})
            except:
                pass # no consideramos al jugador anonimo
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
    
