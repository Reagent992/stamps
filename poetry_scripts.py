import subprocess


def dr():
    """Запуск сервера разработки."""
    cmd = ["python", "manage.py", "runserver"]
    subprocess.run(cmd)


def ds():
    """Запуск Django Shell."""
    cmd = ["python", "manage.py", "shell"]
    subprocess.run(cmd)


def cw():
    """Запуск Celery worker."""
    cmd = ["python", "-m", "celery", "-A", "config", "worker", "-l", "info"]
    subprocess.run(cmd)


def rb():
    """Запуск контейнера с RabbitMQ."""
    cmd = [
        "docker",
        "run",
        "-it",
        "--rm",
        "--name",
        "rabbitmq",
        "-p",
        "5672:5672",
        "-p",
        "15672:15672",
        "rabbitmq:management",
    ]
    subprocess.run(cmd)


def flower():
    """Run Flower."""
    cmd = ["python", "-m", "celery", "-A", "config", "flower"]
    subprocess.run(cmd)
