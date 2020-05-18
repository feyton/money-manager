from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'money_manager',
        'HOST': 'localhost',
        'PASSWORD': 'admin',
        'USER': 'postgres'
    }
}
