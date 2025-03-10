from .base import *
from environs import Env

# env= environs.Env()

env = Env()              # Get os environ
env.read_env(BASE_DIR / ".env")   # Read .env file

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','127.0.0.1', 'localhost']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" 
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_ADDRESS","")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD","")
DEFAULT_FROM_EMAIL = "PronixFX Academy <noreply@yourdomain.com>"