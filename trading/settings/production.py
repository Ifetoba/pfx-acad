from .base import *

import environs

env = environs.Env()              # Get os environ
env.read_env(BASE_DIR / ".env")   # Read .env file

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

DATABASES = {

}

MIDDLEWARE += [
    
]