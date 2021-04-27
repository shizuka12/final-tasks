from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

# Create your tests here.


username = "already_exist"
username2 = "new_username"

class Signup_Tests(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(username, '', 'password_a')
        user.save()

    '''
    もしUserCreationFormのusernameがまだ登録されていないもので、
    password1とpassword2が一致し、かつ条件を満たした文字列であれば,
    form.is_valid()はTrueになり、topにリダイレクトする
    '''
    def test_newusername_and_correct_password(self): 
        form = UserCreationForm({'username': username2, 'password1': 'password_b', 'password2': 'password_b'})
        self.assertTrue(form.is_valid())
        data = {
            'username': username2,
            'password': 'password_b'
        }
        response = self.client.post(reverse('accounts:signin'), data=data)
        self.assertRedirects(response, reverse('accounts:top'))

    '''
    もしUserCreationFormのusernameが既に登録されたものであれば,
    form.is_valid()はFalseになる
    '''
    def test_already_existed_name(self):
        form = UserCreationForm({'username': username, 'password1': 'password_b', 'password2': 'password_b'})
        self.assertFalse(form.is_valid())

    '''
    もしUserCreationFormのusernameが登録されていないものだとしても、
    password1とpassword2が一致しなければform.is_valid()はFalseになる
    '''
    def test_with_dismatch_password(self):
        form = UserCreationForm({'username': username2, 'password1': 'password_b', 'password2': 'password_c'})
        self.assertFalse(form.is_valid())
    
    '''
    もしUserCreationFormのpasswordが短いものだと、
    form.is_valid()はFalseになる
    '''
    def test_with_short_password(self):
        form = UserCreationForm({'username': username2, 'password1': 'pass_b', 'password2': 'pass_b'})
        self.assertFalse(form.is_valid())
    
    '''
    UserCreationFormに登録すると、
    データベースにユーザーが保存される
    '''
    def test_save_of_user(self):
        form = UserCreationForm({'username': username2, 'password1': 'password_b', 'password2': 'password_b'})
        form.save()
        self.assertTrue(User.objects.filter(username='new_username').exists())


class Signin_Tests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username, '', 'password_a')
        user.save()

    '''
    登録済みのユーザーがログインした時に、
    form.is_valid()はTrueになり、topにリダイレクトする。
    '''
    def test_with_correct_user(self):
        form = AuthenticationForm(data = {'username': username, 'password': 'password_a'})
        self.assertTrue(form.is_valid())
        data = {
            'username': username,
            'password': 'password_a'
        }
        response = self.client.post(reverse('accounts:signin'), data=data)
        self.assertRedirects(response, reverse('accounts:top'))

    '''
    登録されていないユーザーがログインした時に、
    form.is_valid()はFalseになる。
    '''
    def test_with_not_existed_user(self):
        form = AuthenticationForm(data = {'username': username2, 'password': 'password_b'})
        self.assertFalse(form.is_valid())
