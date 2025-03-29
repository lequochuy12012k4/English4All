from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = 'django-insecure-$z=f6s3u(jz=q3%z-^i$=ho7=_*y*j$0$qf2^_9mc)hlc=za*#'

DEBUG = True

ALLOWED_HOSTS = ['english4all.onrender.com','localhost']

SITE_ID = 2

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',  
]

SOCIAL_ACCOUNT_PROVIDERS = {
    "google":{
        "SCOPE":{
            "profile",
            "email"
        },
        "AUTH_PARAMS": {"access_type": "online"}
    },
    "github":{
        "SCOPE":{
            "profile",
            "email"
        },
        "AUTH_PARAMS": {"access_type": "online"}
    },
    "facebook":{
        "SCOPE":{
            "profile",
            "email"
        },
        "AUTH_PARAMS": {"access_type": "online"}
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'english_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'english_web.wsgi.application'

DATABASES = {
    "default":{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME':'mydatabase'
    }
    # "default": {
    #     'ENGINE':'django.db.backends.postgresql',
    #     'NAME':'railway',
    #     'USER':'postgres',
    #     'PASSWORD':os.environ.get('DB_PASSWORD'),  
    #     'HOST':'tramway.proxy.rlwy.net',
    #     'PORT':'49047'
    # }
}
database_url = 'postgresql://english4all_zeog_user:1PSYBK1o05gyFLrauN9RImkgO5LTcGam@dpg-cvjsg99r0fns739jor10-a.singapore-postgres.render.com/english4all_zeog'
DATABASES['default'] = dj_database_url.parse(database_url)

# Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'app/static',  # Adjust this path if necessary
]
STATIC_ROOT = BASE_DIR / 'productionfiles'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENITICATION_BACKENDS = {
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
}
import os
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ... other settings ...

# Google API Key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Add logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR,'app/static/images')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'lequochuy12012k4@gmail.com'
EMAIL_HOST_PASSWORD = 'lfnb wrdi ixoy ywqw'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
