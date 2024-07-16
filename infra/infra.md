# Логика работы docker в проекте.
- **Celery** работает в одном контейнере с **Django**, т.к. так проще, выносить ее в отдельный контейнер сейчас нету необходимости.
- Везде используются сокращения **dev** и **prod**.
- Используется стратегия "Merge Compose files". т.е. есть базовый `compose.yml` и он расширяется файлом `compose.override.yml` для **dev** и файлом `compose.prod.yml` для **prod**.
- Переменные окружения завязанные на dev/prod уже прописаны.

## dev
Запуск: `docker compose up` - запустится сразу `compose.yml` и `compose.override.yml` который расширяет его до **dev** версии.

- Создается superuser с **login**: admin **password**: admin
  login и password берутся из environment variables в `compose.override.yml`, там их можно заменить.
- Рабочий каталог вмонтирован в образ. Это позволяет автоматически перезагружаться серверу разработки.

## prod
Запуск: `docker compose -f compose.yml -f compose.prod.yml up` - базовый файл и расширяющий его. __Последовательность важна!__
