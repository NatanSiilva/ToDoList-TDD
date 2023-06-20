import random
import getpass
from fabric import Connection
from fabric import Config
from fabric import SerialGroup as Group
from fabric import Result

REPO_URL = "https://github.com/NatanSiilva/ToDoList-TDD.git"


def deploy():
    host = 'superlists-staging.natandev.com.br'
    site_folder = "/home/deploy/sites/" + host
    source_folder = site_folder + "/source"

    key_path = "/media/natanael/434026ea-8088-4930-9960-92d9e137c8d945/@home/natanael/Documents/docs/host-jenkins.pem"
    key_passphrase = getpass.getpass("SSH Key Passphrase: ")

    config = Config(
        overrides={
            "sudo": {"password": getpass.getpass("SSH Password for 'deploy' user: ")}
        }
    )
    conn = Connection(
        host,
        config=config,
        connect_kwargs={"key_filename": key_path, "passphrase": key_passphrase},
    )

    # _create_directory_structure_if_necessary(conn, site_folder)
    _get_latest_source(conn, source_folder)
    _update_settings(conn, source_folder, host)
    _update_virtualenv(conn, source_folder)
    _update_static_files(conn, source_folder)
    _update_database(conn, source_folder)


def _create_directory_structure_if_necessary(conn, site_folder):
    conn.run(f"mkdir -p {site_folder}/database")
    conn.run(f"mkdir -p {site_folder}/static")
    conn.run(f"mkdir -p {site_folder}/virtualenv")
    conn.run(f"mkdir -p {site_folder}/source")


def _get_latest_source(conn, source_folder):
    if conn.run(f"test -d {source_folder}/.git", warn=True).failed:
        conn.run(f"git clone {REPO_URL} {source_folder}")
    else:
        with conn.cd(source_folder):
            conn.run("git fetch")
            current_commit = conn.local("git log -n 1 --format=%H", capture=True)
            conn.run(f"git reset --hard {current_commit}")


def _update_settings(conn, source_folder, site_name):
    settings_path = f"{source_folder}/superlists/settings.py"
    conn.sed(settings_path, "DEBUG = True", "DEBUG = False")
    conn.sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = f"{source_folder}/superlists/secret_key.py"

    if conn.run(f"test -e {secret_key_file}", warn=True).failed:
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        conn.append(secret_key_file, f'SECRET_KEY = "{key}"')

    conn.append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(conn, source_folder):
    virtualenv_folder = f"{source_folder}/../virtualenv"

    if conn.run(f"test -e {virtualenv_folder}/bin/pip", warn=True).failed:
        conn.run(f"python3.6 -m venv {virtualenv_folder}")

    conn.run(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_static_files(conn, source_folder):
    with conn.cd(source_folder):
        conn.run("../virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database(conn, source_folder):
    with conn.cd(source_folder):
        conn.run("../virtualenv/bin/python manage.py migrate --noinput")
