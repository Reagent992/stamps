# Проект интернет-магазина по изготовлению печатей и штампов на заказ
- [Проект интернет-магазина по изготовлению печатей и штампов на заказ](#проект-интернет-магазина-по-изготовлению-печатей-и-штампов-на-заказ)
  - [Описание](#описание)
  - [Зависимости](#зависимости)
    - [Основные зависимости](#основные-зависимости)
    - [dev зависимости](#dev-зависимости)
  - [Запуск проекта](#запуск-проекта)
    - [dev](#dev)
    - [prod](#prod)
  - [Автор](#автор)
  - [Модель БД](#модель-бд)
## Описание

![Картинка-Пример](images/img.png)
- Проект находится в разработке.
## Зависимости

### Основные зависимости
| Библиотека                                                                        | Версия | Описание                                                    |
| --------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------- |
| python                                                                            | 3.10   | Язык программирования Python версии                         |
| django                                                                            | 4      | Фронт на Джанго-шаблонах                                    |
| celery                                                                            | latest | Очередь задач                                               |
| rabbitmq                                                                          | latest | Брокер для celery                                           |
| flower                                                                            | latest | Трекер для celery задач                                     |
| django-view-breadcrumbs                                                           | latest | "Хлебные крошки", breadcrumbs для отображения "пути".       |
| django-ckeditor                                                                   | 5      | Редактор теста                                              |
| python-slugify                                                                    | latest | Транслитерация текста                                       |
| Poetry                                                                            | latest | Пакетный менеджер                                           |
| Environs[django]                                                                  | latest | Для хранения секретов в файле `.env`                        |
| django-json-widget                                                                | latest | Для удобного просмотра и редактирования JSONField           |
| django-crispy-forms(c crispy_bootstrap5)                                          | latest | Для Генерации форм                                          |
| bootstrap                                                                         | 5      | CSS                                                         |
| pillow                                                                            | latest | images                                                      |
| sorl-thumbnail                                                                    | latest | images thumbnails                                           |
| [django-ckeditor-5](https://github.com/hvlads/django-ckeditor-5)                  | 5      | Редактор текста для админки                                 |
| django-dirtyfields                                                                | latest | Отслеживание изменений в объекте модели, до сохранения в БД |
| gunicorn                                                                          | latest | wsgi-сервер                                                 |
| [django-split-settings](https://github.com/wemake-services/django-split-settings) | latest | Позволяет разделять настройки на несколько файлов           |
| sentry                                                                            | latest | Отслеживание ошибок                                         |

### dev зависимости
| Библиотека                                               | Версия | Описание                                                                |
| -------------------------------------------------------- | ------ | ----------------------------------------------------------------------- |
| pre-commit                                               | latest | Автоматический запуск black, isort, flake8 при использование git commit |
| black, isort, flake8                                     | latest | Code Style                                                              |
| django-debug-toolbar                                     | latest | Оверлей для разработки.                                                 |
| django-stubs[compatible-mypy]                            | latest | typehints                                                               |
| djlint                                                   | latest | Линтер для Django-шаблонов                                              |
| selenium                                                 | latest | Функциональные тесты                                                    |
| [Factory Boy](https://github.com/FactoryBoy/factory_boy) | latest | Generate fake, test data                                                |

## Запуск проекта
- Везде используются сокращения **dev** и **prod**.
- Используется стратегия "Merge Compose files". т.е. есть базовый `compose.yml` и он расширяется файлом `compose.override.yml` для **dev** и файлом `compose.prod.yml` для **prod**.
- Переменные окружения завязанные на dev/prod уже прописаны.

### dev
1. Запуск: `docker compose up` - запустится сразу `compose.yml` и `compose.override.yml` который расширяет его до **dev** версии.
2. Запуск `djnago runserver` и `celery worker`.\
Для этого есть короткие команды создаваемые `poetry`:
     - `dwc` (django with celery)
     - `dr`(django run)
     - `cw`(celery worker)
3. Доступны management команды для создания фикстур:
   -  `python manage.py fixture` - Для создания фикстур.
   -  `python manage.py delete` - Для отчистки таблиц в которые были добавлены фикстуры.
- Создается superuser с **login**: admin **password**: admin\
  login и password берутся из environment variables в `compose.override.yml`, там их можно заменить.


### prod
Запуск: `docker compose -f compose.yml -f compose.prod.yml up` - базовый файл и расширяющий его. __Последовательность важна!__
- **Celery** работает в одном контейнере с **Django**, т.к. так проще, выносить ее в отдельный контейнер сейчас нету необходимости.
## Автор

[Sadykov Miron](https://github.com/Reagent992)


## Модель БД

<details>
  <summary>Модель БД от руки</summary>
  <img src="images/models.png" alt="Модель БД от руки">
  Так же доступен оригинальный файл в excalidraw-формате.

</details>
<details>
  <summary>Модель БД от pg_admin</summary>
  <img src="images/db_by_pg_admin.png" alt="Модель БД от pg_admin">

</details>
