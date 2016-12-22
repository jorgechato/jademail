import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
        '0.0.0.0',
        'localhost',
        'nas.jorgechato.com',
        '192.168.1.20',
        '192.168.1.21',
        '192.168.1.11',
        ]


# Application definition
INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'sendgrid',
        'ckeditor',
        'import_export',
        'crispy_forms',
        'grid',
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

ROOT_URLCONF = 'jademail.urls'

LOGIN_REDIRECT_URL = 'grid:home'
LOGIN_URL = 'login'
redirect_unauthenticated_users = True
CRISPY_TEMPLATE_PACK = 'bootstrap3'

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
                ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    ],
                },
            },
        ]

WSGI_APPLICATION = 'jademail.wsgi.application'

# Password validation
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
LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Ckeditor config
CKEDITOR_CONFIGS = {
        'default': {
            'skin': 'moono',
            'toolbar_OrggueToolbar': [
                {'name': 'document', 'items': ['Source', '-', 'Save',
                    'NewPage', 'Preview', 'Print', '-', 'Templates']},
                {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste',
                    'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {'name': 'links', 'items': ['Link', 'Unlink']},
                {'name': 'insert', 'items': ['Image','Upload', 'Table',
                    'HorizontalRule', 'Smiley', 'SpecialChar']}, '/',
                {'name': 'basicstyles', 'items': [
                    'Bold', 'Italic', 'Underline', 'Strike',
                    'Subscript', 'Superscript', '-', 'RemoveFormat']},
                {'name': 'paragraph', 'items': [
                    'NumberedList', 'BulletedList', '-', 'Outdent',
                    'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                    'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                    'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language']},
                {'name': 'colors', 'items': ['TextColor', 'BGColor']},
                {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
                {'name': 'styles', 'items': ['Styles', 'Format', 'FontSize']},
                ],
            'toolbar': 'OrggueToolbar',
            'tabSpaces': 4,
            'extraPlugins': ','.join(
                [
                    'image2',
                    'div',
                    'autolink',
                    'autoembed',
                    'embedsemantic',
                    'autogrow',
                    'widget',
                    'lineutils',
                    'clipboard',
                    'dialog',
                    'dialogui',
                    'elementspath'
                    ]),
                }
        }
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_JQUERY_URL = "https://code.jquery.com/jquery-3.1.1.min.js"

# 10MB - 10485760
MAX_UPLOAD_SIZE = "10485760"

try:
    from local_settings import *
except ImportError:
    pass
