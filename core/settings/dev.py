from .base import *

DEBUG = os.environ.get('DEBUG').lower() != "false"
ALLOWED_HOSTS = [
    '*'
]

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:1337']
