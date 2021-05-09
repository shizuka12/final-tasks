from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib.auth import login, logout

# Create your tests here.


username = "already_exist"
username2 = "new_username"

class Signup_Tests(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(username, '', 'password_a')

    def test_newusername_and_correct_password(self): 
        '''
        もしUserCreationFormのusernameがまだ登録されていないもので、
        password1とpassword2が一致し、かつ条件を満たした文字列であれば,
        form.is_valid()はTrueになり、topにリダイレクトする
        '''
        data = {
            'username': username2,
            'password1': 'password_b',
            'password2': 'password_b'
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('accounts:signup'), data=data)
        user_info = User.objects.get(username=username2)
        self.assertRedirects(response, reverse('tmitter:top', args=str(user_info.id)))

    def test_already_existed_name(self):
        '''
        もしUserCreationFormのusernameが既に登録されたものであれば,
        form.is_valid()はFalseになる
        '''        
        form = UserCreationForm({'username': username, 'password1': 'password_b', 'password2': 'password_b'})
        self.assertFalse(form.is_valid())

    def test_with_dismatch_password(self):
        '''
        もしUserCreationFormのusernameが登録されていないものだとしても、
        password1とpassword2が一致しなければform.is_valid()はFalseになる
        '''
        form = UserCreationForm({'username': username2, 'password1': 'password_b', 'password2': 'password_c'})
        self.assertFalse(form.is_valid())
    
    def test_with_short_password(self):
        '''
        もしUserCreationFormのpasswordが短いものだと、
        form.is_valid()はFalseになる
        '''
        form = UserCreationForm({'username': username2, 'password1': 'pass_b', 'password2': 'pass_b'})
        self.assertFalse(form.is_valid())
    
    def test_save_of_user(self):
        '''
        UserCreationFormに登録すると、
        データベースにユーザーが保存される
        '''
        form = UserCreationForm({'username': username2, 'password1': 'password_b', 'password2': 'password_b'})
        form.save()
        self.assertTrue(User.objects.filter(username='new_username').exists())


class Signin_Tests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username, '', 'password_a')
    
    def test_with_correct_user(self):
        '''
        登録済みのユーザーがログインした時に、
        form.is_valid()はTrueになり、topにリダイレクトする。
        '''
        form = AuthenticationForm(data = {'username': username, 'password': 'password_a'})
        self.assertTrue(form.is_valid())
        data = {
            'username': username,
            'password': 'password_a'
        }
        response = self.client.post(reverse('accounts:signin'), data=data)
        user_info = User.objects.get(username=username)
        self.assertRedirects(response, reverse('tmitter:top', args=str(user_info.id)))

    def test_with_not_existed_user(self):
        '''
        登録されていないユーザーがログインした時に、
        form.is_valid()はFalseになる。
        '''
        form = AuthenticationForm(data = {'username': username2, 'password': 'password_b'})
        self.assertFalse(form.is_valid())


class Signout_Tests(TestCase):
    def setUp(self):
        data = {
            'username': username,
            'password': 'password_a'
        }
        user = User.objects.create_user(data)
        self.client.login(data=data)
    
    def test_redirect_after_signout(self):
        '''
        ログアウトしたら、ログインページにリダイレクトされる
        '''
        response = self.client.post(reverse('accounts:signout'))
        self.assertRedirects(response, reverse('accounts:signin'))
