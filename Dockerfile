# BASED ON https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docker/django/Dockerfile

FROM python:3.10.14-slim-bookworm AS python-base

# Needed for fixing permissions of files created by Docker:
ARG PROD=True \
  UID=1000 \
  GID=1000

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.8.3 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'


RUN apt-get update \
  && apt-get upgrade -y \
  && pip install --upgrade pip \
  && apt-get install --no-install-recommends -y \
  bash \
  curl \
  git \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # cleaning up
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# user config
RUN groupadd -g "${GID}" -r web \
  && useradd -d '/app' -g web -l -r -u "${UID}" web \
  && chown web:web -R '/app'

# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /app/

# Project initialization:
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$PROD" \
  && poetry version \
  # Install deps:
  && poetry run pip install -U pip \
  && poetry install \
  $(if [ "$PROD" = True ]; then echo '--only main'; fi) \
  --no-interaction --no-ansi --sync

COPY /infra/django/entrypoint /entrypoint
# converts Windows line endings to UNIX line endings.
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY /infra/django/start_dev /start_dev
RUN sed -i 's/\r$//g' /start_dev
RUN chmod +x /start_dev

COPY /infra/django/start_prod /start_prod
RUN sed -i 's/\r$//g' /start_prod
RUN chmod +x /start_prod

COPY /infra/django/celery-worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY /infra/django/celery-flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

ENTRYPOINT ["/entrypoint"]

# Production image
FROM python-base AS prod

COPY . .
