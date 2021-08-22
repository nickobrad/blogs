from .. import db
from flask_login import UserMixin, login_manager, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login_manager
from datetime import date, datetime

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):

    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(255))
    secondname = db.Column(db.String(255))
    username = db.Column(db.String(255),unique = True)
    email = db.Column(db.String(255), unique = True, index = True) 
    profile_picture = db.Column(db.String())
    profile_bio = db.Column(db.String(255))
    secured_password = db.Column(db.String(255))
    blog_posts_by_me = db.relationship('Blog', backref = 'myblogposts', lazy = 'dynamic')
    blog_comments_by_me = db.relationship('BlogComment', backref = 'myblogcomments', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot view a users password')

    @password.setter
    def password(self, password):
        self.secured_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secured_password, password)

    @classmethod
    def save_user(self):
        db.session.add(self)
        db.session.commit()