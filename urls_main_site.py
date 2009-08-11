import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from contributable_games.views import *

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^register/$', register, name='register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contributable_games/login.html'}, name='login'),
    url(r'^login_to_game/(?P<game_name>.*)/$', login_to_game, name='login_to_game'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', profile, name='profile'),
    url(r'^create_game/$', create_game, name='create_game'),
    url(r'^edit_game/(?P<object_id>.*)/$', edit_game, name='edit_game'),
    url(r'^$', index, name='index'),        
)
