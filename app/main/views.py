from flask import render_template, request, redirect, url_for, abort
from flask.helpers import flash
from . import main
from .. import db, photos
from flask_login import login_required, current_user
from ..models.user import User
from ..models.blog_post import Blog
from ..models.blog_comment import BlogComment
from app.main.forms import BlogPostCommentForm, BlogPostForm
from ..requests import get_quote


@main.route('/home')
@login_required
def home():
    title = "Welcome to Blogs"
    quote = get_quote()
    blogs2 = db.session.execute(
        'SELECT * FROM blogs ORDER BY date_posted ASC;'
    ).all()
    blogs = Blog.query.all()
    return render_template('index.html', title = title, blogs = blogs, quote = quote)

@main.route('/post/blog', methods = ['GET', 'POST'])
@login_required
def post_blog():

    post_blog_form = BlogPostForm()
    title = "Post a blog"

    if post_blog_form.validate_on_submit():
        title = post_blog_form.blog_title.data
        blog = post_blog_form.blog_post.data
        blog_post = Blog(blog_title = title, blog_posted = blog, user_id = current_user.id)
        db.session.add(blog_post)
        db.session.commit()
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
            
    return redirect(url_for('main.profile', id = user.id))

@main.route('/blog/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update_blog(id):

    blogs = Blog.query.filter_by(id = id).first()

    if request.method == 'post':
        title = request.form['title']
        blog = request.form['blog']
        error = None

        if not title:
            error = 'A blog title is required'

        if error is not None:
            flash(error)
        else:
            db.session(
                'UPDATE blogs SET blog_title = ?, blog_posted = ?'
                'WHERE id = ?',
                (title, blog,id)
            )
            db.commit()
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
