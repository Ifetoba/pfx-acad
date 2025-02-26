# import environs
from .base import *
from environs import Env

# env= environs.Env()

env = Env()              # Get os environ
env.read_env(BASE_DIR / ".env")   # Read .env file

SECRET_KEY = env("DJANGO_SECRET_KEY")
STRIPE_PUBLIC_KEY = env("")
ALLOWED_HOSTS = []

DATABASES = {

}

MIDDLEWARE += [
    
]

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" 
# EMAIL_HOST = "smtp.mailgun.org"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "postmaster@yourdomain.com"
# EMAIL_HOST_PASSWORD = "your-mailgun-api-key"
# DEFAULT_FROM_EMAIL = "PronixFX Academy <noreply@yourdomain.com>"