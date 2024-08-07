import subprocess
from concurrent.futures import ThreadPoolExecutor


def dr():
    """Запуск сервера разработки."""
    cmd = ["python", "manage.py", "runserver"]
    subprocess.run(cmd, cwd="src")


def dt():
    """Запуск Django Test."""
    cmd = ["python", "manage.py", "test"]
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


def flower():
    """Run Flower."""
    cmd = ["python", "-m", "celery", "-A", "config", "flower"]
    subprocess.run(cmd, cwd="src")


def dwc():
    """Запуск Django с celery worker в одном thread."""

    def run_command(cmd):
        subprocess.run(cmd, cwd="src")

    with ThreadPoolExecutor() as executor:
        executor.submit(
            run_command,
            ["python", "manage.py", "runserver"],
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
