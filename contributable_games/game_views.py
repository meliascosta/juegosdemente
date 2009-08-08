import time, re, os
from datetime import date, datetime
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from models import Game, GamePage, GameResource, SavedPlay, LogEntry
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import LazyUser
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from woozp_utils.view import json_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from cStringIO import StringIO

GAME_COOKIE_NAME = "game_sessionid"

def with_game_session(view):
    def decorated(request, *args, **kargs):
        game = get_object_or_404(Game, name=kargs['game_name'])
        engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        session_key = request.GET.get('sessionid', None) or request.COOKIES.get(GAME_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)
        
        request.game = game
        response = view(request, *args, **kargs)
        
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            # Save the session data and refresh the client cookie.
            request.session.save()
            response.set_cookie(GAME_COOKIE_NAME,
                    request.session.session_key, max_age=None,
                    expires=None, domain=settings.SESSION_COOKIE_DOMAIN,
                    path=reverse('serve_game_index', args=[game.name]),
                    secure=settings.SESSION_COOKIE_SECURE or None)
        return response
        
    return decorated

@with_game_session
def game_login(request, game_name):
    if not request.user.is_authenticated():
        request.session.save(must_create=True)
        next = reverse('share_main_cookie', args=[game_name, request.session.session_key])
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('serve_game_index', args=[game_name]))

@with_game_session
def game_logout(request, game_name):
    return logout(request, reverse('serve_game_index', args=[game_name]))

@login_required
def share_main_cookie(request, game_name, game_session_key):
    engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    game_session = engine.SessionStore(game_session_key)
    for x in SESSION_KEY, BACKEND_SESSION_KEY:
        game_session[x] = request.session[x]
    game_session.save()
    return HttpResponseRedirect(reverse('serve_game_index', args=[game_name])+'?sessionid='+game_session_key)

def serve_game_resource(request, game_name, resource_path):
    game = get_object_or_404(Game, name=game_name)
    res = get_object_or_404(GameResource, game=game, file=game.resource_path+resource_path)
    return serve(request, resource_path, document_root=settings.MEDIA_ROOT+game.resource_path)

valid_tags = ['username', 'logout_url', 'login_url', 'js_includes']
parser = re.compile('{{ (?=%s)(.*?) }}' % '|'.join(valid_tags))

@with_game_session
def serve_game_page(request, game_name, page_path):
    page = get_object_or_404(GamePage, game=request.game, file=request.game.page_path+page_path)
    js_includes = render_to_string('contributable_games/js_includes.html',
                                   {'SETTINGS':settings, 'game_name':game_name, 'user':request.user})
    
    tag_values = {'username': request.user.username or '~Anonimo',
                  'js_includes': js_includes,
                  'logout_url': reverse('game_logout', args=[game_name]),
                  'login_url': reverse('game_login', args=[game_name]),}
    return HttpResponse(parser.sub(lambda x: unicode(tag_values[x.group(1)]), page.file.read()))

@with_game_session
def new_play(request, game_name):
    profile = request.user.profile if request.user.is_authenticated() else None
    obj = SavedPlay.objects.create(profile = profile, ip = request.META['REMOTE_ADDR'],
                                   game = request.game, score = 0)
    request.session['current_play_id_for_%s' % game_name] = obj.id
    return json_to_response({'play_id': obj.id})

@with_game_session
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
    
@with_game_session
def set_score(request, game_name):
    play = get_object_or_404(SavedPlay, pk=request.session['current_play_id_for_%s' % game_name])
    
    play.score = request.POST['score']
    play.save()
    return json_to_response({'status':200})
