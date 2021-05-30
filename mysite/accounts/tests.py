from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from .models import Follow
from django.shortcuts import get_object_or_404
import time

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
        self.assertRedirects(response, reverse('tmitter:top'))

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
        self.assertRedirects(response, reverse('tmitter:top'))

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


class FollowViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.user2 = User.objects.create_user("username2", "", "password_b")
        self.client.login(username="username1", password='password_a')
    
    def test_follow_database(self):
        '''
        フォローしたらデータベースに追加される
        ''' 
        request = reverse('accounts:follow', args=str(2))
        self.client.post(request)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())
    
    def test_follow_myself(self):
        '''
        自分自身をフォローすることはできない
        '''
        url = reverse('accounts:follow', args=str(1))
        self.client.post(url)
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user1).exists())
    
    def test_follow_redirect(self):
        '''
        フォローしたらアカウントページにリダイレクトする
        '''
        response = self.client.post(reverse('accounts:follow', args=str(2)))
        self.assertRedirects(response, reverse('tmitter:accountpage', args=str(2)))


class UnfollowViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.user2 = User.objects.create_user("username2", "", "password_b")
        self.user3 = User.objects.create_user("username3", "", "password_c")
        self.client.login(username="username1", password='password_a')
        Follow.objects.create(follower_id=1, following_id=2)
        Follow.objects.create(follower_id=1, following_id=3)
    
    def test_unfollow_database(self):
        '''
        フォロー解除したらデータベースから削除される
        '''
        url = reverse('accounts:unfollow', args=str(2))
        self.client.post(url)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user3).exists())

    def test_unfollow_redirect(self):
        '''
        フォロー解除したらアカウントページにリダイレクトする
        '''
        response = self.client.post(reverse('accounts:unfollow', args=str(2)))
        self.assertRedirects(response, reverse('tmitter:accountpage', args=str(2)))


class Folllower_detailViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.user2 = User.objects.create_user("username2", "", "password_b")
        self.user3 = User.objects.create_user("username3", "", "password_c")
        Follow.objects.create(follower_id=2, following_id=1)
        time.sleep(0.1)
        Follow.objects.create(follower_id=3, following_id=1)
        self.client.login(username="username1", password='password_a')

    def test_follower_list(self):
        '''
        follower_detailにアクセスすると、
        そのアカウントのフォロワーが表示される
        '''
        follower_id_list = [3, 2]
        response = self.client.get(reverse('accounts:follower_detail', args=str(1)))
        self.assertContains(response, Follow.objects.values('follower__username').all())


class Folllowing_detailViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.user2 = User.objects.create_user("username2", "", "password_b")
        self.user3 = User.objects.create_user("username3", "", "password_c")
        Follow.objects.create(follower_id=1, following_id=2)
        time.sleep(0.1)
        Follow.objects.create(follower_id=1, following_id=3)
        self.client.login(username="username1", password='password_a')

    def test_folloing_list(self):
        '''
        following_detailにアクセスすると、
        そのアカウントがフォローしているアカウントが表示される
        '''
        following_id_list = [3, 2]
        response = self.client.get(reverse('accounts:following_detail', args=str(1)))
        queryset = response.context['following_list']
        for i in range(2):
            self.assertEqual(queryset[i].following_id, following_id_list[i])
