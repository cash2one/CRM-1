# -*- coding: utf-8 -*-

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4h(rd31g^q(#vpv!7a_q-!1sc+v(#1e0qaiuh2ja98ly4mj&2='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['192.168.22.108','10.20.0.242', 'crm.100credit.cn', '0.0.0.0', '127.0.0.1', 'localhost']
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'crm.100credit.cn', '192.168.162.103']

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'easy_thumbnails',
    'bootstrap3',
    'i_bankserver',
    'accounts',
    'crm',
    'export',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'www.urls'

WSGI_APPLICATION = 'www.wsgi.application'

# INTERNAL_IPS = ['10.20.0.202']


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'crm',
#         'USER': 'crm',
#         'PASSWORD':'Crm_2015-06-25',
#         # 'HOST':'192.168.162.101',
#         'HOST':'localhost',
#         'PORT':'3306',
#         'OPTIONS':  {
#             'init_command': 'SET storage_engine=MyISAM;',
#         },
#     },
#     'bank_server_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bankServer3',
#         'USER': 'bank3_Crm_Select',
#         'PASSWORD': 'BankServer3_CrM_SelEct_2016.03.24',
#         'HOST': '192.168.22.26',
#         'PORT': '3306',
#     },
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crm',
        'USER': 'crm',
        'PASSWORD': '7552735535',
        #'HOST': '192.168.162.103',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET storage_engine=MyISAM;',
        },
    },
    'bank_server_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bankServer3',
        'USER': 'bankServer3',
        'PASSWORD': '20150911',
        'HOST': '192.168.162.109',
        'PORT': '3306',
    },
 }


# use multi-database in django
DATABASE_ROUTERS = ['database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    'i_bankserver': 'bank_server_db',
}

# Internationalization

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False


THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (120, 120), 'crop': True},
    },
}

# Static files (CSS, JavaScript, Images)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERY_URL': 'http://cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
# }


# email settings
# EMAIL_HOST = 'smtp.100credit.com'
EMAIL_HOST = '117.121.48.85'
EMAIL_PORT = 25
# EMAIL_HOST_USER = 'crmtest@100credit.com'
# EMAIL_HOST_PASSWORD = 'OGUlHhKjMW'
EMAIL_HOST_USER = 'crm@100credit.com'
EMAIL_HOST_PASSWORD = 'HrDZINyOr9'
EMAIL_SUBJECT_PREFIX = u'[CRM]'
EMAIL_USE_TLS = True


# False:会话cookie可以在用户浏览器中保持有效期;True:关闭浏览器,则Cookie失效.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60*60*24  # 一天

LOGDIR = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGDIR, 'error.log'),    # 日志输出文件
            'maxBytes': 1024*1024*5,                          # 文件大小
            'backupCount': 5,                                 # 备份份数
            'formatter': 'standard',                          # 使用哪种formatter日志格式
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'crm_error': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
