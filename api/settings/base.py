# coding: utf-8

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's%_j3%2s%3pm%^!#ma!46g_6y08!r**)!3u8$8-04t0w&emj6s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'pagseguro',
    'payment',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'paymentserver',
        'USER': 'root',
        'PASSWORD': '',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_REPLACE_HTTPS_REFERER = False
CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'Authorization',
        'x-csrftoken'
    )
CORS_ORIGIN_WHITELIST = (
        'localhost',
        '127.0.0.1',
    )

CIELO_SANDBOX_AFFILIATION_ID = '1006993069'
CIELO_SANDBOX_API_KEY = '25fbb99741c739dd84d7b06ec78c9bac718838630f30b112d033ce2e621b34f3'
CIELO_AFFILIATION_ID = ''
CIELO_API_KEY = ''

REDECARD_URL_PROD = 'https://ecommerce.userede.com.br/pos_virtual/wskomerci/cap.asmx'
REDECARD_URL_DEV = 'https://ecommerce.userede.com.br/pos_virtual/wskomerci/cap_teste.asmx'
REDECARD_SANDBOX_AFFILIATION_ID = '123456789'
REDECARD_AFFILIATION_ID = ''

PAGSEGURO_EMAIL = 'victorluna22@gmail.com'
PAGSEGURO_TOKEN = '0D12C3907E6540E196771B03240674FA'
PAGSEGURO_SANDBOX = False
PAGSEGURO_LOG_IN_MODEL = True # se o valor for True, os checkouts e transacões vão ser logadas no database.

# PAYPAL_TEST = True
# PAYPAL_WPP_USER = "victorluna22-facilitator_api1.gmail.com"
# PAYPAL_WPP_PASSWORD = "1402944428"
# PAYPAL_WPP_SIGNATURE = "Am.1ly7-pWkc7Y59220DtdIjXe7QAVEfUXqeuh3G-EU.WveiOBsv7dwM"