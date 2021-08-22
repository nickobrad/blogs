from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_simplemde import SimpleMDE


db = SQLAlchemy()
bootstrap = Bootstrap()
photos = UploadSet('photos', IMAGES)
mail = Mail()
simple = SimpleMDE()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = ''

def create_app(config_name):
    #Initializing application
    app = Flask(__name__)

    #Setting up configuration
    app.config.from_object(config_options[config_name])

    # Initializing Flask Extensions
    # bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .authentication import authentication as authentication_blueprint
    app.register_blueprint(authentication_blueprint)

    from .blog_update import blogpost as blogpost_blueprint
    app.register_blueprint(blogpost_blueprint)

    # Configure UploadSet
    configure_uploads(app, photos)

    # Setting config
    from .requests import configure_request
    configure_request(app)

    return app