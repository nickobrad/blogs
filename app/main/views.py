from flask import render_template, request, redirect, url_for, abort
from flask.helpers import flash
from . import main
from .. import db, photos
from flask_login import login_required, current_user
from ..models.user import User
from ..models.blog_post import Blog
from ..models.blog_comment import BlogComment
from ..models.subscribers import Subscribers
from app.main.forms import BlogPostCommentForm, BlogPostForm, SubscriberForm
from ..requests import get_quote
from ..email import mail_message


@main.route('/home', methods = ['POST','GET'])
@login_required
def home():
    subscribe_form = SubscriberForm()

    title = "Welcome to Blogs"
    quote = get_quote()
    blog = db.session.execute(
        'SELECT * FROM blogs ORDER BY date_posted DESC;'
    ).all()
    blogs = Blog.query.all()


    if subscribe_form.validate_on_submit():
        firstname = subscribe_form.firstname.data
        lastname = subscribe_form.lastname.data
        email = subscribe_form.email.data
        new_subscriber = Subscribers(firstname = firstname, lastname = lastname, email  = email)
        db.session.add(new_subscriber)
        db.session.commit()
        return redirect(url_for('main.home'))
        
    return render_template('index.html', title = title, blogs = blogs, quote = quote, subscribe_form = subscribe_form)

@main.route('/post/blog', methods = ['GET', 'POST'])
@login_required
def post_blog():

    users = User.query.all()
    post_blog_form = BlogPostForm()
    title = "Post a blog"

    if post_blog_form.validate_on_submit():
        title = post_blog_form.blog_title.data
        blog = post_blog_form.blog_post.data
        blog_post = Blog(blog_title = title, blog_posted = blog, user_id = current_user.id)
        db.session.add(blog_post)
        db.session.commit()

        for user in users:
            mail_message("New Post on Blogzy", "email/newpost", user.email, user = user, user2 = blog_post.myblogposts.username)

        return redirect(url_for('main.home'))
    
    return render_template('post_blog.html', post_blog_form = post_blog_form, title = title)

@main.route('/post/blog/<int:id>/comment', methods = ['GET', 'POST'])
@login_required
def make_comment(id):

    blog_comment_form = BlogPostCommentForm()
    blog_post = Blog.query.filter_by(id = id).first()
    blog_post_comments = BlogComment.query.filter_by(blog_id = id).all()

    title = f'Comment on {blog_post.blog_title}'

    if blog_comment_form.validate_on_submit():
        blog_comment = blog_comment_form.comment.data
        new_blog_comment = BlogComment(comment = blog_comment, blog_id = blog_post.id, user_id = current_user.id )
        db.session.add(new_blog_comment)
        db.session.commit()
        return redirect(url_for('main.theblog', id = new_blog_comment.blog_id))

@main.route('/view/blog/<int:id>', methods = ['POST', 'GET'])
@login_required
def theblog(id): 

    blog_comment_form = BlogPostCommentForm()
    blog_post = Blog.query.filter_by(id = id).first()
    blog_post_comments = BlogComment.query.filter_by(blog_id = id).all()

    title = f'{ blog_post.blog_title }'

    if blog_comment_form.validate_on_submit(): 
        blog_comment = blog_comment_form.comment.data
        new_blog_comment = BlogComment(comment = blog_comment, blog_id = blog_post.id, user_id = current_user.id )
        db.session.add(new_blog_comment)
        db.session.commit()
        return redirect(url_for('main.theblog'))

    return render_template('theblog.html', blog_comment_form = blog_comment_form, blog = blog_post, blog_comments = blog_post_comments)

@main.route('/profile/<int:id>', methods = ['GET', 'POST'])
@login_required
def my_profile(id):

    user = User.query.filter_by(id = id).first()
    title = f'{user.username}\'s Profile'

    if user is None:
        abort(404)

    myblogs = Blog.query.filter_by(user_id = id).all()
    mycomments = BlogComment.query.filter_by(user_id = id).all()

    return render_template('/profile/profile.html', myblogs = myblogs, mycomments = mycomments, title = title, user = user)

@main.route('/profile/update', methods = ['GET', 'POST'])
@login_required
def update_profile():

    user = User.query.filter_by(id = current_user.id).first()
    title = f'Update {user.username}\'s Profile'

    if user is None:
        abort(404)

    if request.files:
        if request.files['photo'] != "":
            filename = photos.save(request.files['photo'])
            path = f'profile_pictures/{filename}'
            user.profile_picture = path
            db.session.add(user)
            db.session.commit()
        else:
            return redirect(url_for('main.my_profile', id = user.id))
            
    return redirect(url_for('main.my_profile', id = user.id))

@main.route('/blog/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update_blog(id):

    blogs = Blog.query.filter_by(id = id).first()

    if request.form:
        title = request.form['title']
        blog = request.form['blog'] 
        blogs.blog_title = title
        blogs.blog_posted = blog
        db.session.commit()
        return redirect(url_for('main.my_profile', id = current_user.id))
        
    return render_template('update_blog.html', blogs = blogs)

@main.route('/profile/update/delete')
@login_required
def delete_post():

    user = User.query.filter_by(id = current_user.id).first()
    myblogs = Blog.query.filter_by(id = current_user.id).first()
    db.session.delete(myblogs)
    db.session.commit()

    return redirect(url_for('main.my_profile', id = current_user.id))

@main.route('/delete/comment/<int:id>')
@login_required
def delete_comment(id):

    blogcomment = BlogComment.query.filter_by(id = id).first()
    db.session.delete(blogcomment)
    db.session.commit()

    return redirect(url_for('main.theblog', id = blogcomment.blog_id))

