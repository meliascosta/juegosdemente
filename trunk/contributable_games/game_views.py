from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from models import Game, SavedPlay, LogEntry, Profile
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from woozp_utils.view import json_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from woozp_utils.json import json_encode
from cStringIO import StringIO
from django.views.static import serve
from os import path
from datetime import date
from django.utils.encoding import force_unicode


def game_login(request, game_name):
    '''
    Creates a new sessionkey and pass it to the main domain so it can validate it.
    '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.MAIN_SITE_XD_LOGIN)
    return HttpResponseRedirect(reverse('serve_game_index', args=[game_name]))

def game_logout(request, game_name):
    request.session['LOGOUT'] = True;
    return HttpResponseRedirect(settings.MAIN_SITE_DOMAIN)

def serve_game_page(request, game_name, page_path):
    game = request.game
    score =  0;
    state = [0];
    if request.user.is_authenticated():
        if request.user.profile.is_school_player:
            if request.user.profile.last_session_date == date.today():
                return HttpResponseRedirect(settings.MAIN_SITE_DOMAIN)
        maxPlay = SavedPlay.objects.filter(profile=request.user.profile).order_by('-score')
        score = maxPlay[0].score if len(maxPlay)>0 else 0
        state = simplejson.loads(request.user.profile.current_state)
    full_path = game.abs_pages_path+page_path
    if path.isfile(full_path):
        page = file(full_path, 'r')
    else:
        return HttpResponseNotFound("This game doesn't have a %s page" % page_path)
    js_includes = render_to_string('contributable_games/js_includes.html', {
        'SETTINGS': settings,
        'game': game,
        'user': request.user,
        'game_files': game.game_files,
        'login_url': game.login_url,
        'state': state[game.name] if game.name in state else [0,0],
        'score': score 
    })
    return HttpResponse(force_unicode(page.read()).replace('{{ js_includes }}', js_includes))

def new_play(request, game_name):
    profile = request.user.profile if request.user.is_authenticated() else None
    obj = SavedPlay.objects.create(profile = profile, ip = request.META['REMOTE_ADDR'],
                                   game = request.game, score = 0)
    request.session['current_play_id_for_%s' % game_name] = obj.id
    return json_to_response({'play_id': obj.id})

def log_action(request, game_name):
    play = get_object_or_404(SavedPlay, pk=request.session['current_play_id_for_%s' % game_name])
    
    log = request.POST.get('log','')
    for line in StringIO(log.encode('utf-8')):
        ev = simplejson.JSONDecoder().decode(line)
        entry = LogEntry(savedplay=play, type=ev['type'],
                         ms=ev['time'], order=ev['order'], _data='')
        entry.data = ev['data']
        entry.save()
    
    return json_to_response({'status':200})
    
def set_score(request, game_name):
    play = get_object_or_404(SavedPlay, pk=request.session['current_play_id_for_%s' % game_name])
    if request.user.is_authenticated():
        user = get_object_or_404(Profile, username=request.user.profile.username)
        state = simplejson.JSONDecoder().decode(user.current_state)
        state[game_name] = request.GET.getlist('state')
        user.current_state = simplejson.dumps(state)
        user.save()
    if play.score < int(request.GET['score']):
        play.score = request.GET['score']
        play.save()
    return json_to_response({'status':200})
    

def get_score(request, game_name):
    g = Game.objects.filter(name=game_name)[0]
    ranking = []
   
    for rank in g.ranking:
        try:
            ranking.append({'name': rank['profile'].username,'score':rank['score']})
        except:
            pass #no existe el jugador
    return json_to_response(ranking)

def school_end_stage(request,game_name):
    user = get_object_or_404(Profile, username=request.user.profile.username)
    user.last_session_date = date.today()
    user.current_school_game = user.current_school_game+1
    user.save()
    return json_to_response({'status':200})
    
def _serve_game_path(request, directory, filename):
    if not path.exists(settings.MEDIA_ROOT+directory+filename):
        raise Http404("File Not Found")
    return serve(request, filename, document_root=settings.MEDIA_ROOT+directory)

def serve_game_resource(request, game_name, resource_path):
    return _serve_game_path(request, request.game.resource_path, resource_path)

def serve_game_file(request, game_name, game_file_path):
    return _serve_game_path(request, request.game.game_file_path, game_file_path)