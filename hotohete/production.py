import dj_database_url
from hotohete.settings import *

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = [
    'hotohete.herokuapp.com',
    'hotohetestaging.herokuapp.com'
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

SECRET_KEY = os.environ['SECRET_KEY']

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
