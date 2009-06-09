import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from contributable_games.views import serve_game_resource, serve_game_page, register, profile, index

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    #/main/* urls internas
    url(r'^register/$', register, name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contributable_games/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', profile, name='login'),
    url(r'^$', index, name='index'),
        
    #/<mijuego>/* son urls propias de cada juego.
    url(r'^games/(?P<game_name>.*)/res/(?P<resource_path>.*)$',
        serve_game_resource, name="serve_game_static"),
    url(r'^games/(?P<game_name>.*)/(?P<page_path>.*)/$',
        serve_game_page, name="serve_game_page")
)
