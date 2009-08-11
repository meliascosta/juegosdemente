import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from contributable_games.game_views import game_login, game_logout,\
    serve_game_resource, serve_game_page, new_play, log_action, set_score

urlpatterns = patterns('',
    url(r'^(?P<game_name>.*)/login/', game_login, name="game_login"),
    url(r'^(?P<game_name>.*)/logout/', game_logout, name="game_logout"),
    url(r'^(?P<game_name>.*)/new_play/', new_play, name="new_play"),
    url(r'^(?P<game_name>.*)/log_action/', log_action, name="log_action"),
    url(r'^(?P<game_name>.*)/set_score/', set_score, name="set_score"),
    url(r'^(?P<game_name>.*)/res/(?P<resource_path>.*)',
        serve_game_resource, name="serve_game_static"),
    url(r'^(?P<game_name>.*)/$', serve_game_page,
        {'page_path':'index.html'}, name="serve_game_index"),
    url(r'^(?P<game_name>.*)/(?P<page_path>.*)',
        serve_game_page, name="serve_game_page"),
)