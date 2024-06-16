FROM python:3.10-slim

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# get rid of poetry in container since it's slow down the build process a lot.
RUN apt-get update \
  && apt-get upgrade -y \
  # dependencies for building Python packages
  # && apt-get install -y build-essential \
  # psycopg2 dependencies
  # && apt-get install -y libpq-dev \
  # Translations dependencies
  # && apt-get install -y gettext \
  # Additional dependencies
  # && apt-get install -y git \
  # curl and poetry
  # && apt-get -y install curl \
  # && curl -sSL https://install.python-poetry.org | python3 - \
  # && export PATH="/root/.local/bin:$PATH" \
  # && poetry --version \
  # cleaning up unused files
  && pip install --upgrade pip \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# poetry env variable
# ENV PATH="/root/.local/bin:$PATH"
# COPY poetry.lock .
# COPY pyproject.toml  .
# # dependencies
# RUN poetry install

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

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


# user config
RUN adduser --disabled-password --no-create-home django
USER django


ENTRYPOINT ["/entrypoint"]
