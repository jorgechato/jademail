# JedEmail

Email assistant to help you to send a bunch of emails from your account.
This is NOT set for advertisement or SEO, it uses your own email and credentials to send emails.

## Install
```zsh
$ pip install -r requirements.txt
```

## Run
```zsh
$ py manage.py runserver 0.0.0.0:8000
```

## local_settings.py
```python
from settings import os, BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = "uploads/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            }
        }

SENDGRID_API_KEY = ''
```

## Email template
In the email template should be three variables *{{TITLE}} {{TO}} {{CONTENT}}*, as you can see in the following lines.
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title></title>
</head>
<body>
  <h1>{{TITLE}}</h1>
  Dear {{TO}},
  {{CONTENT}}
</body>
</html>
```

## [Demo]()
The demo does not include sending a message, the porpouse of the demo is just get confortable with the interface and see the template of the email.
**User: ** demo
**Pass: ** jademail

## Project structure
```zsh
.
├── grid
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   ├── email_form.html
│   │   ├── grid
│   │   │   ├── list_form.html
│   │   │   ├── list_list.html
│   │   │   ├── person_detail.html
│   │   │   ├── person_form.html
│   │   │   ├── person_list.html
│   │   │   ├── template_detail.html
│   │   │   ├── template_form.html
│   │   │   └── template_list.html
│   │   └── pagination.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── jademail
│   ├── forms.py
│   ├── __init__.py
│   ├── local_settings.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── manage.py
├── README.md
├── requirements.txt
└── templates
    ├── accounts
    │   └── login.html
    ├── _layouts
    │   └── base.html
    └── _modules
        ├── messages.html
        └── nav.html
```
