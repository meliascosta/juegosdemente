import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from contributable_games.views import serve_game_resource, serve_game_page

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    #/<mijuego>/* son urls propias de cada juego.
    url(r'^(?P<game_name>.*)/res/(?P<resource_path>.*)$',
        serve_game_resource, name="serve_game_static"),
    url(r'^(?P<game_name>.*)/(?P<page_path>.*)/$',
        serve_game_page, name="serve_game_page")
)
