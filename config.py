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

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/blogs'


class DevConfig(Config):

    UPLOADED_PHOTOS_DEST ='app/static/profile_pictures'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/blogs'
    DEBUG = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('RANDOM_URI')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DATABASE = 'd7fjuql4lnqec9'
    POSTGRES_USER = 'exawszgayavjbf'
    POSTGRES_PASSWORD = 'bfb19b743e3241198149e5ea2f33396c0b835e952bc467160521c71dfe543bc7'


class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://omondii:2325@localhost/blogstest'



config_options = {'development':DevConfig,'production':ProdConfig, 'test':TestConfig}