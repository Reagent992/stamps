FROM python:3.10-slim as python-base

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app


RUN apt-get update \
  && apt-get upgrade -y \
  && pip install --upgrade pip \
  # cleaning up
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*


COPY infra/requirements/prod.txt infra/requirements/dev.txt ./



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


# Production image
FROM python-base as prod
RUN pip install -r prod.txt \
&& pip cache purge

# user config
RUN adduser --disabled-password --no-create-home django
USER django

ENTRYPOINT ["/entrypoint"]

# Development image
FROM python-base as dev
RUN pip install -r dev.txt \
&& pip cache purge

# user config
RUN adduser --disabled-password --no-create-home django
USER django

ENTRYPOINT ["/entrypoint"]
