from os import getenv, path
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import timedelta

def load_dot_env():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)


class Config:
    load_dot_env()

    PORT = getenv('PORT', 8080)
    DEBUG = True

    dev = getenv('IS_DEV', False)

    DB_USER = getenv('DB_USER', 'wmsflask')
    DB_PASSWORD = getenv('DB_PASSWORD', 'wmsflask')
    DB_HOST = getenv('DB_HOST', '127.0.0.1')
    DB_PORT = getenv('DB_PORT', 3306)
    DB_NAME = getenv('DB_NAME', 'wmsflask')

    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    BASE_DIR = path.abspath(dirname(__file__))

    # application threads
    THREADS_PER_PAGE = getenv('THREADS_PER_PAGE', 2)

    # protection against CSRF
    CSRF_ENABLED = getenv('CSRF_ENABLED', True)
    CSRF_SESSION_KEY = getenv('CSRF_SESSION_KEY', 'secret')  # TODO: secret key for signing data

    # secret key for signing cookies
    SECRET_KEY = getenv('SECRET_KEY', 'VerySecret')

    # Key for API JWT tokens
    JWT_SECRET_KEY = 'TOPSECRET'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
