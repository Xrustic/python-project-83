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

Запускаем приложение ```make dev```

Для автоматического деплоя есть файл ```build.sh``` который нужно будет указать на сервисе деплоя.


## Вид сайта
- После команды ```make dev```, у нас появится ссылка на [сайт](http://127.0.0.1:5000).

- Нажав на кнопку 'Запустить проверку', если все правильно, нас перенаправит на страницу с информацией о сайте.

- Так же мы можем перейти на вкладки 'Сайт' и 'Анализатор страниц'.
Кнопка 'Анализатор страниц', отправит нас обратно на главный сайт, где мы сможем ввести еще один url для проверки.

- После чего нас опять отправит на сайт, с проверками. Где мы так же можем 'Запустить проверку'.

- Кнопка 'Сайт', будет переносить нас на страницу, где мы сможем посмотреть все сайты, которые мы добавляли, их проверки и код ответа.


## Пример работы сайта
![alt text](https://raw.githubusercontent.com/Xrustic/files_for_projects/main/projct-83/project_83.gif)
