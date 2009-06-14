from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from models import Game, GamePage, GameResource, Profile
from django.shortcuts import get_object_or_404, render_to_response
import re, os
from datetime import date, datetime
from woozp_utils.view import AjaxView, request_response
from django import forms

def index(request):
    return render_to_response('contributable_games/index.html',{'games': Game.objects.all(),'users':User.objects.all()})

def profile(request):
    return request_response(request, 'contributable_games/profile.html')

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

register = user_passes_test(lambda x: not x.is_authenticated(), login_url="/")(Register())

def serve_game_resource(request, game_name, resource_path):
    game = get_object_or_404(Game, name=game_name)
    res = get_object_or_404(GameResource, game=game, name=resource_path)
    return serve(request, resource_path, document_root=settings.MEDIA_ROOT+game.resource_path)

valid_tags = ['date', 'datetime']
parser = re.compile('{{ (?=%s)(.*?) }}' % '|'.join(valid_tags))

def serve_game_page(request, game_name, page_path):
    game = get_object_or_404(Game, name=game_name)
    page = get_object_or_404(GamePage, game=game, name=page_path)
    
    tag_values = {'date': date.today(), 'datetime':datetime.now()}
    return HttpResponse(parser.sub(lambda x: unicode(tag_values[x.group(1)]), page.file.read()))
