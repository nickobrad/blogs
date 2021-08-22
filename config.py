import os
import secrets

class Config:

    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    UPLOADED_PHOTOS_DEST ='app/static/profile_pictures'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    QUOTE_API_URL =  'http://quotes.stormconsultancy.co.uk/random.json'

    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/blogs'


class DevConfig(Config):

    UPLOADED_PHOTOS_DEST ='app/static/profile_pictures'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/blogs'
    DEBUG = True

class ProdConfig(Config):

    pass

class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/blogstest'



config_options = {'development':DevConfig,'production':ProdConfig, 'test':TestConfig}