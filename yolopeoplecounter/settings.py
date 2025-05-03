import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('secretkey')

BD_PASSWORD = os.getenv('bdpassword')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yolo_app',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'yolo_app' / 'static' ]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'yolo_app' / 'static' / 'uploads'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "yolo_app" / "templates" ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

ROOT_URLCONF = 'yolopeoplecounter.urls'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'yolo_db',
        'USER':     'postgres',
        'PASSWORD':  BD_PASSWORD,
        'HOST':     'localhost',
        'PORT':     '5432',
    }
}

DEBUG = True
ALLOWED_HOSTS = []
