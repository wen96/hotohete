from hotohete.settings import *


DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': 'localhost',
    'NAME': 'hotohete',
    'USER': 'hotohete',
    'PASSWORD': 'testtest',
}


# CACHES = {
#     "default": {
#         "BACKEND": "redis_cache.RedisCache",
#         "LOCATION": "127.0.0.1:6379",
#         "OPTIONS": {"DB": 0}
#     }
# }
