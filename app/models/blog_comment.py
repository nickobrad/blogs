from .. import db
from datetime import date, datetime


class BlogComment(db.Model):
    
    __tablename__ = 'blogcomments'  

    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String)
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_posted = db.Column(db.DateTime, default = date.today)

    def save_comment(self):
        db.session.add(self) 
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comment_by_id(cls, id):
        blog_comment = BlogComment.query.filter_by(id = id).first()
        return blog_comment

    @classmethod
    def get_comments_by_user(cls, id):
        comments_by_user = BlogComment.query.filter_by(user_id = id).all()
        return comments_by_user
    