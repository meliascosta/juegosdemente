import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from contributable_games.views import *
from contributable_games.game_views import share_main_cookie, game_login, game_logout,\
    serve_game_resource, serve_game_page, new_play, log_action, set_score
from django.http import HttpResponseRedirect

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    #urls internas
    url(r'^main/register/$', register, name='register'),
    url(r'^main/accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contributable_games/login.html'}, name='login'),
    url(r'^main/login_to_game/(?P<game_name>.*)/(?P<game_session_key>.*)/$', share_main_cookie, name='share_main_cookie'),
    url(r'^main/accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^main/accounts/profile/$', profile, name='profile'),
    url(r'^main/create_game/$', create_game, name='create_game'),
    url(r'^main/edit_game/(?P<object_id>.*)/$', edit_game, name='edit_game'),
    url(r'^main/$', index, name='index'),
    url(r'^$', lambda x: HttpResponseRedirect('/main/')),
        
    #/<mijuego>/* son urls propias de cada juego.
    url(r'^games/(?P<game_name>.*)/login/', game_login, name="game_login"),
    url(r'^games/(?P<game_name>.*)/logout/', game_logout, name="game_logout"),
    url(r'^games/(?P<game_name>.*)/new_play/', new_play, name="new_play"),
    url(r'^games/(?P<game_name>.*)/log_action/', log_action, name="log_action"),
    url(r'^games/(?P<game_name>.*)/set_score/', set_score, name="set_score"),
    url(r'^games/(?P<game_name>.*)/res/(?P<resource_path>.*)',
        serve_game_resource, name="serve_game_static"),
    url(r'^games/(?P<game_name>.*)/$', serve_game_page,
        {'page_path':'index.html'}, name="serve_game_index"),
    url(r'^games/(?P<game_name>.*)/(?P<page_path>.*)',
        serve_game_page, name="serve_game_page"),
)
