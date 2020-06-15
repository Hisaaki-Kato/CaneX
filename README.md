
# CaneX

# Requirement
* python 3.6.9
* MySQL 14.14

### pip libraries
* Django 3.0.4
* django-mysql 3.5.0
* mysqlclient 1.4.6
* numpy 1.18.2
* pandas 1.0.3

# Usage
## MySQL

MySQLを起動し、シェルに移動します。

```bash
sudo service mysql start
>> * Starting MySQL database server mysqld 

sudo mysql -u root -p
```
パスワードを求められますが、初回はEnterを押せば入れます。

mysql内でrootユーザーのパスワードを設定し、databaseを作成してください。

```bash
mysql>update mysql.user set password=password('root用の任意パスワード') where user = 'root';
mysql>create database canex;
```
databaseが作成されたことを確認し、退出します。
```bash
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| canex '←作成された' |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
mysql>exit
```
## local_settings.py
projectのフォルダに移動し、local_settings.pyを作成します。
```bash
cd /CaneX/CaneXproject
touch local_settings.py
```
local_settings.py中身
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '(h!gd7cd=w-wqya1s%9u@b!kg(n+h*8uivj#l#lh*%pu@aj-xw'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'canex',
        'USER': 'root',
        'PASSWORD': 'root用の任意パスワード',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

## db migration
manage.pyが存在するフォルダに移動し、下記を実行してください。
```bash
python manage.py makemigrations
python manage.py migrate
```

## runserver
下記を実行し、サーバーが立ち上がれば終了です。
```bash
python manage.py runserver
```

# Note
local_settings.py内のSECRET_KEYは流出するとまずいので、リポジトリをパブリックにはしないでください。

# Author

*[@Hisaaki-Kato](https://github.com/Hisaaki-Kato)