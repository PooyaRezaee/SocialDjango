from .base import *

DEBUG = os.environ.get('DEBUG').lower() != "false"
ALLOWED_HOSTS = [
    '*'
]