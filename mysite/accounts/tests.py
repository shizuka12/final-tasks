from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your tests here.


username = "already_exist"
username2 = "new_username"

class Signup_Tests(TestCase):
  
  def setUp(self):
    user = User.objects.create_user(username, '', 'pass_a')
    user.save()

  '''
  もしUserCreationFormのusernameがまだ登録されていないもので、
  password1とpassword2が一致し、かつ条件を満たした文字列であれば,
  form.is_valid()はTrueになる 
  '''
  def test_newusername_and_correct_password(self): 
    form = UserCreationForm({'username': username2, 'password1': 'pass_b', 'password2': 'pass_b'})
    self.assertTrue(form.is_valid)

  '''
  もしUserCreationFormのusernameが既に登録されたものであれば,
  form.is_valid()はFalseになる
  '''
  def test_already_existed_name(self):
    form = UserCreationForm({'username': username, 'password1': 'pass_b', 'password2': 'pass_b'})
    self.assertFalse(form.is_valid())

  '''
  もしUserCreationFormのusernameが登録されていないものだとしても、
  password1とpassword2が一致しなければform.is_valid()はFalseになる
  '''
  def test_with_dismatch_password(self):
    form = UserCreationForm({'username': username2, 'password1': 'pass_b', 'password2': 'pass_c'})
    self.assertFalse(form.is_valid())

