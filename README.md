
python3 -m venv env

env\Scripts\activate.bat
source env/bin/activate
env\Scripts\activate
cd project

# 01_cereat_project_and_api_app

01- py -m venv env

02- django-admin startproject project

03- cd project

04- python manage.py runserver

05- python manage.py startapp api


06- 

إضافة التطبيق إلى إعدادات المشروع



INSTALLED_APPS = [
    # التطبيقات الافتراضية
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # التطبيقات المضافة
    'myapp',
]





07- python manage.py runserver





# 02_createsuperuser

1- python manage.py migrate

2- python manage.py createsuperuser

admin - admin 

3- python manage.py runserver



# 03 install Django REST Framework & knox

1- pip install djangorestframework

2- pip install django-rest-knox


3-
INSTALLED_APPS = [
    ...
    'rest_framework',
    'knox',
    ...
]


4- 

REST_FRAMEWORK = {
 
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    
    ],

}












