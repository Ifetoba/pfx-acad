# import environs
from .base import *
from environs import Env

# env= environs.Env()

env = Env()              # Get os environ
env.read_env(BASE_DIR / ".env")   # Read .env file

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {

}

MIDDLEWARE += [
    
]

HANDLER404 = "users.views.custom_404_view"

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" 
# EMAIL_HOST = "smtp.mailgun.org"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "postmaster@yourdomain.com"
# EMAIL_HOST_PASSWORD = "your-mailgun-api-key"
# DEFAULT_FROM_EMAIL = "PronixFX Academy <noreply@yourdomain.com>"

STRIPE_PUBLIC_KEY = env("")