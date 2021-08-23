from .. import db

class Subscribers(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String, nullable = False)
    lastname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)