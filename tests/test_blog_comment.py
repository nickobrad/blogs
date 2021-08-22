import unittest
from app.models.user import User
from app.models.blog_comment import BlogComment
from app.models.blog_post import Blog 
from app import db

class BlogCommentTest(unittest.TestCase):
    
    def tearDown(self):
        BlogComment.query.delete()
        Blog.query.delete()
        User.query.delete()
 
    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.user_James = User(id = 20, username = 'James',secured_password = 'potato', email = 'james@ms.com')
        self.new_blog_post = Blog(id = 20, blog_posted = "This is a good day", date_posted = "14/11/2020", user_id = self.user_James.id, upvote = 0, downvote = 0)
        self.new_blog_comment= BlogComment(id = 20, comment = "Very nice", blog_id = 20, user_id = self.user_James.id, date_posted = "14/08/2020")

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog_comment.id,20)
        self.assertEquals(self.new_blog_comment.blog_id,20)
        self.assertEquals(self.new_blog_comment.comment,"Very nice")
        self.assertEquals(self.new_blog_comment.user_id,self.user_James.id)
        self.assertEquals(self.new_blog_comment.date_posted,"14/08/2020")

    def test_save_comment(self):
        db.session.add_all([self.user_James, self.new_blog_post, self.new_blog_comment])
        db.session.commit()
        self.new_blog_comment.save_comment()
        self.assertTrue(len(Blog.query.all()) == 1)

    def test_get_comment_by_id(self):
        db.session.add_all([self.user_James, self.new_blog_post, self.new_blog_comment])
        db.session.commit()
        got_comment = BlogComment.get_comment_by_id(20)
        self.assertTrue(got_comment is not None)

    def test_get_comments_by_user(self):
        db.session.add_all([self.user_James, self.new_blog_post, self.new_blog_comment])
        db.session.commit()
        comments_by_user = BlogComment.get_comments_by_user(20)
        self.assertTrue(comments_by_user is not None)

    def test_delete_comment(self):
        db.session.add_all([self.user_James, self.new_blog_post, self.new_blog_comment])
        db.session.commit()
        self.new_blog_comment.delete_comment()
        self.assertTrue(len(BlogComment.query.all()) == 0)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog_comment, BlogComment))


