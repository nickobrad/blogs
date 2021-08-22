import unittest
from app.models.user import User
from app.models.blog_comment import BlogComment
from app.models.blog_post import Blog 
from app import db

class PitchTest(unittest.TestCase):
    
    def tearDown(self):
        Blog.query.delete()
        User.query.delete() 
 
    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.user_James = User(id = 20, username = 'James',secured_password = 'potato', email = 'james@ms.com')
        self.new_blog_post = Blog(id = 20, blog_posted = "This is a good day", date_posted = "14/11/2020", user_id = self.user_James.id, upvote = 0, downvote = 0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog_post.id,20)
        self.assertEquals(self.new_blog_post.blog_posted,"This is a good day")
        self.assertEquals(self.new_blog_post.date_posted,"14/11/2020")
        self.assertEquals(self.new_blog_post.user_id,self.user_James.id)

    def test_save_blog(self):
        db.session.add_all([self.user_James, self.new_blog_post])
        db.session.commit()
        self.new_blog_post.save_blog_post()
        self.assertTrue(len(Blog.query.all()) == 1)

    def test_delete_blog(self):
        db.session.add_all([self.user_James, self.new_blog_post])
        db.session.commit()
        self.new_blog_post.delete_blog_post()
        self.assertTrue(len(Blog.query.all()) == 0)

    def test_get_blog_by_id(self):
        db.session.add_all([self.user_James, self.new_blog_post])
        db.session.commit()
        got_blog_post = Blog.get_blog_by_id(20)
        self.assertTrue(got_blog_post is not None)

    def test_all_blog_posts_by_user(self):
        db.session.add_all([self.user_James, self.new_blog_post])
        db.session.commit()
        all_blog_posts = Blog.all_blog_posts_by_user(20)
        self.assertTrue(all_blog_posts is not None) 

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog_post, Blog))

