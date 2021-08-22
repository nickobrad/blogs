import unittest
from app.models.user import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_james = User(id = 20, username = 'James', secured_password = 'potato', email = 'james@ms.com')
        self.new_user = User(password = 'banana')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_james, User))

    def test_password_setter(self):
        self.assertTrue(self.new_user.secured_password is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('banana'))