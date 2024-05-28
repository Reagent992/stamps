import subprocess
from concurrent.futures import ThreadPoolExecutor


def dr():
    """Запуск сервера разработки."""
    cmd = ["python", "manage.py", "runserver"]
    subprocess.run(cmd, cwd="src")


def ds():
    """Запуск Django Shell."""
    cmd = ["python", "manage.py", "shell"]
    subprocess.run(cmd, cwd="src")


def dt():
    """Запуск Django Test."""
    cmd = ["python", "manage.py", "test"]
    subprocess.run(cmd, cwd="src")


def mm():
    """Запуск Django MakeMigrations."""
    cmd = ["python", "manage.py", "makemigrations"]
    subprocess.run(cmd, cwd="src")


def cw():
    """Запуск Celery worker."""
    cmd = [
        "python",
        "-m",
        "celery",
        "-A",
        "config",
        "worker",
        "-l",
        "info",
    ]
    subprocess.run(cmd, cwd="src")


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
    subprocess.run(cmd, cwd="src")


def flower():
    """Run Flower."""
    cmd = ["python", "-m", "celery", "-A", "config", "flower"]
    subprocess.run(cmd, cwd="src")


def rc():
    """Run rabbitmq, flower and celery worker at the same terminal window."""

    def run_command(cmd):
        subprocess.run(cmd, cwd="src")

    with ThreadPoolExecutor() as executor:
        executor.submit(
            run_command,
            [
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
            ],
        )
        executor.submit(
            run_command, ["python", "-m", "celery", "-A", "config", "flower"]
        )
        executor.submit(
            run_command,
            [
                "python",
                "-m",
                "celery",
                "-A",
                "config",
                "worker",
                "-l",
                "info",
            ],
        )
