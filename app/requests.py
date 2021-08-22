import urllib.request,json
from .models.quote import Quote
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['SQLALCHEMY_DATABASE_URI'],
        detect_types = sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def configure_request(app):
    global quote_url
    quote_url = app.config['QUOTE_API_URL']

def get_quote():

    with urllib.request.urlopen(quote_url) as url:
        quote_data = url.read()
        quote_response = json.loads(quote_data)

    if quote_response:
        author = quote_response.get('author')
        quote = quote_response.get('quote')
        new_quote = Quote(author, quote)
        return new_quote
    else:
        author = 'Someone out there'
        quote = 'My alarm clock is clearly jealous of my amazing relationship with my bed'
        new_quote = Quote(author, quote)
        return new_quote

