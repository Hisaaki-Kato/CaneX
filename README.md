
# CaneX

This is the web application to visualize a network between vectors.

## sample gif
![demo](https://raw.github.com/wiki/Hisaaki-Kato/CaneX/images/screenshot.gif)

## Description
This application visualizes the Co-occurrence between various vector representations of data. Co-occurrence is determined by calculating the inner product between vectors.

## Features and technical topics

* framework - django

* database - MySQL

* inner-product - numpy

* network visualize - Cytoscape.js

* file upload and delete

## Requirement
* python 3.6.9
* MySQL 5.7

### pip libraries

* Django 3.0.4
* django-mysql 3.5.0
* mysqlclient 1.4.6
* numpy 1.18.2
* pandas 1.0.3

## Setup

### Create db with MySQL

In your MySQL shell, create database named 'canex'.
```sql
mysql> create database canex;
mysql> use canex;
```

## Usage

1. Clone this repository, and move to application directory.
```bash
$ git clone git@github.com:Hisaaki-Kato/CaneX.git
$ cd CaneX
```

2. Move to CaneXproject directory, and create ```local_settings.py```.
```bash
$ cd CaneX/CaneXproject
$ touch local_settings.py
```
The contents of local_settings.py are bellow.
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'Canex_secret_key'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'canex',
        'USER': '---- your mysql user name ----',
        'PASSWORD': '---- your mysql password ----',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

3. Move to the directory where ```manage.py``` exists, and excute db migration.
```bash
$ cd CaneX/
$ python manage.py makemigrations
$ python manage.py migrate
```

4. Excute runserver, and access to localhost.
```bash
$ python manage.py runserver
```

# Author
Hisaaki-Kato