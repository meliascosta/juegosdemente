from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from models import Game, Profile
from django.shortcuts import get_object_or_404, render_to_response
from datetime import date, datetime
from woozp_utils.view import AjaxView, request_response
from django import forms
from django.contrib import admin
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
import zipfile
from unzip import unzip
import tempfile

def index(request):
    return request_response(request, 'contributable_games/index.html',{'games': Game.objects.all(),'users':User.objects.all()})

@login_required
def profile(request):
    return request_response(request, 'contributable_games/profile.html',
                            {'games': request.user.profile.game_set.all()})
class Register(AjaxView):
    HTML = 'contributable_games/register.html'
    
    class Form(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ('username', 'email', 'birthdate', 'gender',)
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
        form = self.Form(request.POST)
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
    fields = ('name', 'title', 'description',)
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
create_game = login_required(CreateGame(Game, users_admin).add_view)
    
class EditGame(UserModelAdmin):
    class form(forms.ModelForm):
        class Meta:
            model = Game
            fields = ('title', 'description', 'zip_file')
        zip_file = forms.FileField()
        
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

edit_game = login_required(EditGame(Game, users_admin).change_view)

def export_game(request, object_id):
    import os
    game = get_object_or_404(Game, pk=object_id)
    zf = zipfile.ZipFile(tempfile.mktemp('_export.zip', '%s_' % game.name), 'w')
    for f in game.files:
        zf.write(str(os.path.join(game.abspath,f)),str(f))
    zf.close()
    return serve(request, zf.filename, document_root='/')

@login_required
def login_to_game(request, game_name):
    engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    game_session = engine.SessionStore(None)
    for x in SESSION_KEY, BACKEND_SESSION_KEY:
        game_session[x] = request.session[x]
    game_session.save()
    url = '%s%s?%s=%s' % (settings.GAMES_SITE_DOMAIN,
                          reverse('serve_game_index', args=[game_name], urlconf="urls_games_site"),
                          settings.LOGIN_KEY_NAME,
                          game_session.session_key)
    return HttpResponseRedirect(url)