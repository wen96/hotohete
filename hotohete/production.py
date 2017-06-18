import dj_database_url
from hotohete.settings import *


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = [
    'hotohete.herokuapp.com'
]
