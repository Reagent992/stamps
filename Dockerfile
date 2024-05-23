FROM python:3.10-slim

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # && apt-get upgrade -y \
  # dependencies for building Python packages
  # && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  # && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git \
  # curl and poetry
  && apt-get -y install curl \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && export PATH="/root/.local/bin:$PATH" \
  && poetry --version \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# poetry env vatiable
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY /infra/django/entrypoint /entrypoint
# converts Windows line endings to UNIX line endings.
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY /infra/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY /infra/django/celery-worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


COPY /infra/django/celery-flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

COPY poetry.lock .
COPY pyproject.toml  .
# dependencies
RUN poetry install


ENTRYPOINT ["poetry", "run", "/entrypoint"]
