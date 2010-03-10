import time
from django.core import urlresolvers
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from models import Game

class SessionMiddleware(object):
    def get_game(self, request):
        resolver = urlresolvers.RegexURLResolver(r'^/', settings.ROOT_URLCONF)
        view, args, kwargs = resolver.resolve(request.path_info)
        return get_object_or_404(Game, name=kwargs['game_name'])
    
    def get_cookie_name(self, game):
        return 'game_session_%s' % game.id
    
    def get_cookie_path(self, game):
        return '/%s' % game.name
    
    def process_request(self, request):
        request.game = game = self.get_game(request)
        engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        session_key = request.GET.get(settings.LOGIN_KEY_NAME, request.COOKIES.get(self.get_cookie_name(game)))
        request.session = engine.SessionStore(session_key)
        

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            logoutflag = request.session.get('LOGOUT',False)
        except (AttributeError,KeyError):
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified or settings.SESSION_SAVE_EVERY_REQUEST or request.GET.get(settings.LOGIN_KEY_NAME):
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                # Save the session data and refresh the client cookie.
                request.session.save()
                response.set_cookie(self.get_cookie_name(request.game),
                        request.session.session_key, max_age=max_age,
                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        path=self.get_cookie_path(request.game),
                        secure=settings.SESSION_COOKIE_SECURE or None)
            if logoutflag:
                for game in Game.objects.all():
                    response.delete_cookie(self.get_cookie_name(game),domain=settings.SESSION_COOKIE_DOMAIN)
        return response
