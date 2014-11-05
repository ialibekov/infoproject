infoproject
===========

Установка и настройка:
1) Используем Django 1.6 и Python2.7
2) Нужно установить South и django-debug-toolbar
3) Для создания пользователя и базы нужно от рута в MySQL выполнить следующие команды 
CREATE USER 'infouser'@'%' IDENTIFIED BY 'infopass';
CREATE DATABASE infodb CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON infodb.* TO 'infouser'@'%' WITH GRANT OPTION;
и команду "python manage.py syncdb" в консоли. При этом Джанга предложит создать суперпользователя(admin), нужно согласиться.
Вот и всё.
