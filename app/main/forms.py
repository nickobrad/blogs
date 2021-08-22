from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, ValidationError, SubmitField
from wtforms.validators import Required, Email, EqualTo
from ..models.user import User
from ..models.blog_post import Blog
from ..models.blog_comment import BlogComment

class BlogPostForm(FlaskForm):
    blog_title = StringField('Your blog post title', validators = [Required()])
    blog_post = TextAreaField('Your blog', validators = [Required()])
    post_blog = SubmitField('Post') 

class BlogPostCommentForm(FlaskForm):
    comment = StringField('Comment here', validators = [Required()])
    post_comment = SubmitField('Comment')