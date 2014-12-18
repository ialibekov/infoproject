infoproject
===========

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

Для установки hunspell: требуется установить пакет hunspell через pip (все зависимости в файле [requirements.txt](requirements.txt)). Сам файл с зависимостями избыточен, так как там есть пакеты, которые на данный момент не используются в проекте. Для того, чтобы pip сумел собрать hunspell ему требуется пакет hunspell-dev, который можно установить через synaptic в Ubuntu или через brew (в данном случае будет просто hunspell) на OSX.

Задачи распределяются через [To-Dos](To-Dos.md). Если есть актуальная задача, следует указать ее там. Там можно видеть план и примерный ход работ. По поводу синтаксиса следует смотреть [сюда.](https://guides.github.com/features/mastering-markdown/)