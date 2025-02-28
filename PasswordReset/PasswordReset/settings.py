# -*- coding: utf-8 -*-
"""
Django settings for PasswordReset project.
Generated by 'django-admin startproject' using Django 1.11.1.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import app.providers
import environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*',   ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PasswordReset.urls'

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

WSGI_APPLICATION = 'PasswordReset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


### CUSTOM settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

LDAP_USER = "ldap-passwd-reset"
KEYTAB_PATH = "../ldap-passwd-reset.keytab"

TOKEN_LEN = 6
TOKEN_LIFETIME = 3600
LIMIT_MAX_VALIDATE_RETRY = 10

LIMIT_MAX_SEND = 3
LIMIT_TIME = 86400


PROVIDERS = {
    "aws-sns-1": {
        "class": app.providers.AmazonSNS,
        "enabled": True,
        "display_name": "SMS",
        "options": {
            "ldap_attribute_name": "telephonenumber",
            # In template {0} will replaced with token
            "msg_template": "Your reset password token: {0} \nDo not tell anyone this code.",
            "aws_key": "",
            "aws_secret": "",
            "aws_region": "eu-west-1",
            "sender_id": "LDAP",
        },
    },
    "email-1": {
        "class": app.providers.Email,
        "enabled": True,
        "display_name": "Email",
        "options": {
            # In template {0} will replaced with token
            "msg_template": "Your reset password token: {0} \nDo not tell anyone this code.",
            "msg_subject": "Your LDAP password reset code",
            "smtp_from": env('SMTP_FROM'), 
            "smtp_user": env('SMTP_USER'),
            "smtp_pass": env('SMTP_PASS'),
            "smtp_server_addr": env('SMTP_SERVER_ADDR'),
            "smtp_server_port": env('SMTP_SERVER_PORT'),
            "smtp_server_tls": True,
        },
    },
    "signal-1": {
        "class": app.providers.Signal,
        "enabled": False,
        "display_name": "Signal",
        "options": {
            "ldap_attribute_name": "telephonenumber",
            # In template {0} will replaced with token
            "msg_template": "Your reset password token: {0} \nDo not tell anyone this code.",
            "sender_number": "+447700900123",
        }
    },
    "slack-1": {
        "class": app.providers.Slack,
        "enabled": False,
        "display_name": "Slack",
        "options": {
            # In template {0} will replaced with token
            "msg_template": "Your reset password token: {0} \nDo not tell anyone this code.",
            # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
            "slack_hook" : "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
            "slack_username" : "announce",
            "slack_icon_emoji" : ":lock:"
        },
    },
}