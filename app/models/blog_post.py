from .. import db
from datetime import date, datetime 

class Blog(db.Model):
    __tablename__ = 'blogs'   

    id = db.Column(db.Integer, primary_key = True) 
    blog_title = db.Column(db.String(255))
    blog_posted = db.Column(db.String) 
    date_posted = db.Column(db.DateTime, default = date.today)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    upvote = db.Column(db.Integer, default = 0)
    downvote = db.Column(db.Integer, default = 0)
    blog_comments = db.relationship('BlogComment', backref = 'commentsontheblog', lazy = "dynamic")

    def save_blog_post(self): 
        db.session.add(self) 
        db.session.commit()

    def delete_blog_post(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_blog_by_id(cls, id):
        blog_post = Blog.query.filter_by(id = id).first()
        return blog_post

    @classmethod
    def all_blog_posts_by_user(cls, id):
        blog_posts = Blog.query.filter_by(user_id = id).all()
        return blog_posts