from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from models import Game, GamePage, GameResource, Profile
from django.shortcuts import get_object_or_404, render_to_response
from datetime import date, datetime
from woozp_utils.view import AjaxView, request_response
from django import forms
from django.contrib import admin

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
    fields = ('name', 'title', 'description', 'image',)
    change_form_template = 'contributable_games/change_object.html'
    
    def has_add_permission(self, request):
        return True
    
    def response_add(self, request, obj):
        super(CreateGame, self).response_add(request, obj)
        return HttpResponseRedirect(reverse('edit_game', args=[obj.id]))
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Creando un nuevo juego'
        return super(CreateGame, self).change_view(request, form_url, extra_context)
    
    def save_model(self, request, obj, form, change):
        obj.profile = request.user.profile
        obj.save()
create_game = login_required(CreateGame(Game, users_admin).add_view)

class GameResourceInline(admin.StackedInline):
    model = GameResource
    extra = 5
    
class GamePageInline(admin.StackedInline):
    model = GamePage
    extra = 5
    
class EditGame(UserModelAdmin):
    fields = ('title', 'description', 'image',)
    change_form_template = 'contributable_games/change_object.html'
    inlines = [GamePageInline,GameResourceInline,]   
    
    def response_change(self, request, obj):
        super(EditGame, self).response_change(request, obj)
        return HttpResponseRedirect('.')
    
    def has_change_permission(self, request, obj):
        return True

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        try:
            obj = Game.objects.get(pk=object_id)
            extra_context['title'] = 'Editando Juego %s' % obj.title
        except Game.DoesNotExist:
            pass #this is also raised and handled inside super's change_view
        return super(EditGame, self).change_view(request, object_id, extra_context)

edit_game = login_required(EditGame(Game, users_admin).change_view)
