from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from models import Game, GamePage, GameResource, SavedPlay, LogEntry, GameFile
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from woozp_utils.view import json_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from woozp_utils.json import json_encode
from cStringIO import StringIO
from django.views.static import serve
from os import path

def game_login(request, game_name):
    '''
    Creates a new sessionkey and pass it to the main domain so it can validate it.
    '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.MAIN_SITE_XD_LOGIN)
    return HttpResponseRedirect(reverse('serve_game_index', args=[game_name]))

def game_logout(request, game_name):
    logout(request, reverse('serve_game_index', args=[game_name]))
    return HttpResponseRedirect(settings.MAIN_SITE_DOMAIN + reverse('logout', urlconf="urls_main_site"))

def serve_game_page(request, game_name, page_path):
    try:
        page = GamePage.objects.get(game=request.game, file=request.game.page_path+page_path)
    except:
        return HttpResponseNotFound("This game doesn't have a %s page" % page_path)
    
    game_files = [path.basename(x.file.name) for x in request.game.gamefile_set.all()]
    
    js_includes = render_to_string('contributable_games/js_includes.html', {
        'SETTINGS':settings,
        'game':request.game,
        'user':request.user,
        'game_files': game_files,
        'logout_url': reverse('game_logout', args=[game_name]),
        'login_url': request.game.login_url,
    })
    
    return HttpResponse(page.file.read().replace('{{ js_includes }}', js_includes))

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
    play.score = request.POST['score']
    play.save()
    return json_to_response({'status':200})

def _serve_game_path(request, cls, directory, filename):
    get_object_or_404(cls, game=request.game, file=directory+filename)
    return serve(request, filename, document_root=settings.MEDIA_ROOT+directory)

def serve_game_resource(request, game_name, resource_path):
    return _serve_game_path(request, GameResource, request.game.resource_path, resource_path)

def serve_game_file(request, game_name, game_file_path):
    return _serve_game_path(request, GameFile, request.game.game_file_path, game_file_path)