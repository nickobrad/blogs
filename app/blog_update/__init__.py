from flask import Blueprint

blogpost = Blueprint('blogpost', __name__)

from . import views, forms