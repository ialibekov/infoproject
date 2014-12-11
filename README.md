infoproject
===========
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/ialibekov/infoproject?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Установка и настройка:

1. Используем Django 1.6 и Python2.7 
2. Нужно установить South и django-debug-toolbar
3. Для создания пользователя и базы нужно от рута в MySQL выполнить следующие команды 
```bash
CREATE USER 'infouser'@'%' IDENTIFIED BY 'infopass';
CREATE DATABASE infodb CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON infodb.* TO 'infouser'@'%' WITH GRANT OPTION;
```
и команду `python manage.py syncdb` в консоли. При этом Django предложит создать суперпользователя(admin), нужно согласиться.

Задачи распределяются через [To-Dos](To-Dos.md). Если есть актуальная задача, следует указать ее там. Там можно видеть план и примерный ход работ. По поводу синтаксиса следует смотреть [сюда.](https://guides.github.com/features/mastering-markdown/)