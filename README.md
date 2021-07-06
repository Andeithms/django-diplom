# Дипломный проект по курсу «Django: создание функциональных веб-приложений»

Для запуска приложения необходимо создать базу данных в postgresql, затем в папке diplom создать config.py, где указать
```
user = 'логин для входа в БД'
password_db = 'пароль от БД'
secret_key = 'любой набор символов'
```
Далее в пустой виртуальной среде выполнить команды:

```
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate
```
И наконец для запуска приложения использовать команду:

```
python manage.py runserver
```


