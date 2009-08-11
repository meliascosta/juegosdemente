from common_settings import *

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'contributable_games.game_session_middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls_games_site'

TEMPLATE_DIRS = (
    ROOT_PATH + '/contributable_games/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media", 
    "django.core.context_processors.request",
    "woozp_utils.template_context_processors.common_template_variables",
    "woozp_utils.template_context_processors.message_from_session",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'contributable_games',
)