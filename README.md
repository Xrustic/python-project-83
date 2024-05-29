# python-project-83
### Github Actions
[![hexlet-check](https://github.com/Xrustic/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Xrustic/python-project-83/actions/workflows/hexlet-check.yml)

### Maintainability Badge
<a href="https://codeclimate.com/github/Xrustic/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/39e9d01fb1dd5eeae2f5/maintainability" /></a>


## Описание

[Page Analyzer](https://python-project-83-20ur.onrender.com "результат можно посмотреть здесь")  – это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с [PageSpeed Insights](https://pagespeed.web.dev/):


## Зависимости

* python >= 3.10
* poetry >= 1.6
* PostgreSQL >= 15.4

## Запуск приложения

Клонируем репозиторий ```git clone https://github.com/Xrustic/python-project-83.git```

Запускаем установку зависимостей ```make install```

Для работы приложения нужны две переменные окружения ```$DATABASE_URL``` и ```$SECRET_KEY```.

Запускаем приложение ```make start```

Для автоматического деплоя есть файл ```build.sh``` который нужно будет указать на сервисе деплоя.