import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '(h!gd7cd=w-wqya1s%9u@b!kg(n+h*8uivj#l#lh*%pu@aj-xw'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'canex',
        'USER': 'root',
        'PASSWORD': 'hisa1101',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]