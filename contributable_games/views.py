from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from models import Game, Profile, SavedPlay
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404, render_to_response
from datetime import date, datetime
from woozp_utils.view import AjaxView, request_response, json_to_response
from django import forms
from django.contrib import admin
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.views import logout
import zipfile
from unzip import unzip
import tempfile

def can_upload_games_required(view):
    def wrapper(request, *args, **kargs):
        if not request.user.profile.can_upload_games:
            raise Http404()
        return view(request, *args, **kargs)
    return wrapper

def main_logout(request):
    logout(request,'/')
    return HttpResponseRedirect(settings.GAMES_SITE_DOMAIN + 'planning/logout/')

def index(request):
    if request.user.is_authenticated():
        if request.user.profile.is_school_player:
            if request.user.profile.last_session_date == date.today():
                return request_response(request,'contributable_games/yajugo.html')
            stages = json.loads(request.user.profile.school_games)
            current = request.user.profile.current_school_game
            return request_response(request,'contributable_games/escuela.html',{'game':stages[current]})
    grosos = top()
    return request_response(request, 'contributable_games/index.html',{'games': Game.objects.all(),'users':User.objects.all(),'grosos':grosos,'games_url':settings.GAMES_SITE_DOMAIN})

def info(request):
    grosos = top()
    return request_response(request, 'contributable_games/info.html',{'grosos':grosos})


@login_required
def profile(request):
    puestos = []
    for game in Game.objects.all():
        try:
            puestos.append({'game':game.title, 'datos':[k for k in game.ranking if k.get('profile') == request.user.profile][0]})
        except IndexError:
            pass # No jugaste a este juego
    return request_response(request, 'contributable_games/profile.html',
                            {'games': request.user.profile.game_set.all(), 'puestos':puestos})

class Register(AjaxView):
    HTML = 'contributable_games/register.html'
    
    class Form(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ('username', 'email', 'birthdate', 'gender','handedness','siblingnumber','siblingorder','avatar')
        password = forms.CharField(widget=forms.PasswordInput())
        password_confirm = forms.CharField(widget=forms.PasswordInput())
    
        def clean_password_confirm(self):
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError("El password y la confirmacion son distintos.")
            return self.cleaned_data['password_confirm']
        
        def save(self):
            ret = super(Register.Form, self).save()
            self.instance.set_password(self.cleaned_data['password'])
            self.instance.save()
            return ret
 
    
    def on_get_call(self, request):
        return request_response(request, self.HTML, {'form': self.Form()})

    def on_post_call(self, request):
        form = self.Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.instance.username, password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        
        return request_response(request, self.HTML, {'form': form})

register = user_passes_test(lambda x: not x.is_authenticated(), login_url="/accounts/profile")(Register())

users_admin = admin.AdminSite('users_admin')

class UserModelAdmin(admin.ModelAdmin):
    def message_user(self, request, message):
        request.session['ok_message'] = message
        
class CreateGame(UserModelAdmin):
    fields = ('name', 'title', 'instructions','description',)
    change_form_template = 'contributable_games/change_object.html'
    
    def has_add_permission(self, request):
        return True
    
    def response_add(self, request, obj):
        super(CreateGame, self).response_add(request, obj)
        return HttpResponseRedirect(reverse('edit_game', args=[obj.id]))
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Creando un nuevo juego'
        return super(CreateGame, self).add_view(request, form_url, extra_context)
    
    def save_model(self, request, obj, form, change):
        obj.profile = request.user.profile
        obj.save()
        obj.create_directory_structure()
create_game = login_required(can_upload_games_required(CreateGame(Game, users_admin).add_view))
    
class EditGame(UserModelAdmin):
    class form(forms.ModelForm):
        class Meta:
            model = Game
            fields = ('title', 'instructions','description', 'zip_file')
        zip_file = forms.FileField(label='Importar', help_text="Importar un archivo .zip exportado previamente")
        
        def clean_zip_file(self):
            zf = zipfile.ZipFile(self.cleaned_data['zip_file'], 'r')
            for name in zf.namelist():
                if '../' in name or name.startswith('/'):
                    raise ValidationError("El archivo zip referencia directorios no accesibles")
                
            return zf
    
    change_form_template = 'contributable_games/edit_game.html'
    
    def response_change(self, request, obj):
        super(EditGame, self).response_change(request, obj)
        return HttpResponseRedirect('.')
    
    def has_change_permission(self, request, obj):
        return request.user.id == obj.profile.id

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        try:
            obj = Game.objects.get(pk=object_id)
            extra_context['title'] = 'Editando Juego %s' % obj.title
        except Game.DoesNotExist:
            pass #this is also raised and handled inside super's change_view
        extra_context['game'] = obj
        return super(EditGame, self).change_view(request, object_id, extra_context)
    
    def save_model(self, request, obj, form, change):
        obj.save()
        unzip(form.cleaned_data['zip_file'], obj.abspath)

edit_game = login_required(can_upload_games_required(EditGame(Game, users_admin).change_view))

def export_game(request, object_id, file_name):
    import os
    game = get_object_or_404(Game, pk=object_id, name=file_name)
    
    zf = zipfile.ZipFile(tempfile.mktemp('export.zip', '%s_' % game.name), 'w')
    import pdb;pdb.set_trace()
    for f in game.files:
        zf.write(str(os.path.join(game.abspath,f)),str(f))
    return serve(request, zf.filename, document_root='/')
    zf.close()

def get_scores(request,game_name):
    g = Game.objects.filter(name=game_name)[0]
    ranking = []
    for rank in g.ranking:
        try:
            ranking.append({'name': rank['profile'].username,'score':rank['score']})
        except:
            pass #no existe el jugador
    return json_to_response(ranking)

@login_required
def login_to_game(request, game_name):
    engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    game_session = engine.SessionStore(None)
    for x in SESSION_KEY, BACKEND_SESSION_KEY:
        game_session[x] = request.session[x]
    game_session.save()
    url = '%s%s?%s=%s' % (settings.GAMES_SITE_DOMAIN,
                          game_name,
                          settings.LOGIN_KEY_NAME,
                          game_session.session_key)
    return HttpResponseRedirect(url)

    
def top():   
    games = Game.objects.all()
    grosos = []
    for game in games:
        ctop = game.ranking[:3]
        for player in ctop:
            if player['profile'] is None: 
                continue
            if ({'name':player.get('profile').username , 'avatar': player.get('profile').avatar.url} not in grosos):
                grosos.append({'name':player.get('profile').username , 'avatar': player.get('profile').avatar.url})
    return grosos  
