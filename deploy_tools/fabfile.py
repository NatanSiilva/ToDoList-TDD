import random
from fabric import Connection, task


REPO_URL = "https://github.com/NatanSiilva/ToDoList-TDD.git"


@task
def deploy(c):
    site_folder = f"/home/deploy/sites/{c.host}"
    source_folder = f"{site_folder}/source"

    _create_directory_structure_if_necessary(c, site_folder)
    _get_latest_source(c, source_folder)
    _update_settings(c, source_folder, c.host)
    _update_virtualenv(c, source_folder)
    _update_static_files(c, source_folder)
    _update_database(c, source_folder)


def _create_directory_structure_if_necessary(c, site_folder):
    c.run(f"mkdir -p {site_folder}/database")
    c.run(f"mkdir -p {site_folder}/static")
    c.run(f"mkdir -p {site_folder}/virtualenv")
    c.run(f"mkdir -p {site_folder}/source")


def _get_latest_source(c, source_folder):
    if c.run(f"test -d {source_folder}/.git", warn=True).failed:
        c.run(f"git clone {REPO_URL} {source_folder}")
    else:
        with c.cd(source_folder):
            c.run("git fetch")
            current_commit = c.local("git log -n 1 --format=%H", capture=True)
            c.run(f"git reset --hard {current_commit}")


def _update_settings(c, source_folder, site_name):
    settings_path = f"{source_folder}/superlists/settings.py"
    c.sed(settings_path, "DEBUG = True", "DEBUG = False")
    c.sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = f"{source_folder}/superlists/secret_key.py"

    if c.run(f"test -e {secret_key_file}", warn=True).failed:
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        c.append(secret_key_file, f'SECRET_KEY = "{key}"')

    c.append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(c, source_folder):
    virtualenv_folder = f"{source_folder}/../virtualenv"

    if c.run(f"test -e {virtualenv_folder}/bin/pip", warn=True).failed:
        c.run(f"python3.6 -m venv {virtualenv_folder}")

    c.run(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_static_files(c, source_folder):
    with c.cd(source_folder):
        c.run("../virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database(c, source_folder):
    with c.cd(source_folder):
        c.run("../virtualenv/bin/python manage.py migrate --noinput")
