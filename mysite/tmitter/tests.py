from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tmeet, Favorite
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import time

# Create your tests here.
class TopViewTests(TestCase):
    def setUp(self):
        self.timeline_list = []
        # username1を作成して、ツミートして、ツミートをリスト追加
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        content = 'This is a timeline test by username1'
        Tmeet.objects.create(author=self.user1, content=content)
        self.timeline_list.append(content)
        # username2を作成して、ツミートして、ツミートをリスト追加
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        content = 'This is a timeline test by username2'
        Tmeet.objects.create(author=self.user2, content=content)
        self.timeline_list.append(content)
        # timeline_listの順番を逆に
        self.timeline_list.reverse()
        # username1としてログイン
        self.client.login(username='username1', password='password_1')
    
    def test_of_timeline(self):
        '''
        トップページにアクセスしたら、
        すべてのユーザーのツミートが新しい順に表示される
        '''
        response = self.client.get(reverse('tmitter:top'))
        queryset = response.context['tmeet_list']
        for i in range(2):
            self.assertEqual(queryset[i].content, self.timeline_list[i])


    def test_top_username(self):
        '''
        ログイン後のトップページに自分の名前がある
        '''
        response = self.client.get(reverse('tmitter:top'))
        self.assertContains(response, self.user1.username)


class AccountpageViewTests(TestCase):
    def setUp(self):
        self.accountpage_list = []
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        for i in range(2):
            content = 'This is an accountpage test' +str(i+1)+ ' by username1'
            Tmeet.objects.create(author=self.user1, content=content)
            time.sleep(0.1)
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        for i in range(2):
            content = 'This is an accountpage test' +str(i+1)+ ' by username2'
            Tmeet.objects.create(author=self.user2, content=content)
            self.accountpage_list.append(content)
            time.sleep(0.1)
        self.accountpage_list.reverse()

    def test_of_tmeetlist(self):
        '''
        アカウントページにアクセスしたら、
        そのユーザーのツミートが新しい順に表示される
        '''
        response = self.client.get(reverse('tmitter:accountpage', kwargs={'user_id': self.user2.pk}))
        queryset = response.context['tmeet_list']
        for i in range(2):
            self.assertEqual(queryset[i].content, self.accountpage_list[i])

    def test_accountpage_username(self):
        '''
        アカウントページに自分の名前がある
        '''
        response = self.client.get(reverse('tmitter:accountpage', kwargs={'user_id': self.user2.pk}))
        self.assertContains(response, self.user2.username)


class DeleteViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')
        content = 'This is a deleteing funtction test1 by username1'
        self.tmeet =Tmeet.objects.create(author=self.user1, content=content)

    def test_of_delete(self):
        '''
        ツミートを削除したらデータベースから削除される
        '''
        self.client.post(reverse('tmitter:delete_tmeet', args=str(self.tmeet.pk)))
        self.assertFalse(Tmeet.objects.filter(author=self.user1, pk=self.tmeet.pk).exists())
    
    def test_delete_redirect(self):
        '''
        ツミートを削除したらアカウントページにリダイレクトする
        '''
        response = self.client.post(reverse('tmitter:delete_tmeet', args=str(self.tmeet.pk)))
        self.assertRedirects(response, reverse('tmitter:accountpage', kwargs={'user_id': self.user1.pk}))


class TmeetModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')

    def test_with_over_length_tmeet(self):
        '''
        140文字以上のツミートは作成できない
        '''
        content = "あいうえおかきくけこ"
        for i in range(14):
            content += "あいうえおかきくけこ"
        test_tmeet = Tmeet.objects.create(author=self.user1, content=content)
        with self.assertRaises(ValidationError):
            test_tmeet.full_clean()


class CreateViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('username1', '', 'password_1')
        self.client.login(username='username1', password='password_1')

    def test_tmeet_redirect(self):
        '''
        ツミートしたらアカウントページにリダイレクトする
        '''
        response = self.client.post(reverse('tmitter:tmeet'), {'content': 'this is test_tmeet_rqedirect'})
        self.assertRedirects(response, reverse('tmitter:accountpage', kwargs={'user_id': self.user1.pk}))
    
    def test_by_another_user(self):
        '''
        別のユーザーになりすましてツミートすることはできない
        '''
        self.user2 = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        self.client.post(reverse('tmitter:tmeet'), {'content': 'this is test_tmeet_rqedirect', 'author': self.user1})
        self.assertFalse(Tmeet.objects.filter(author=self.user1).exists())


class FavoriteViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.tmeet = Tmeet.objects.create(author=self.user1, content='This is a tmeet for favorite test.')
        self.client.login(username="username1", password='password_a')
    
    def test_favorite_database(self):
        '''
        お気に入りにしたらデータベースに追加される
        '''
        self.client.post(reverse('tmitter:favorite'), data={'pk': self.tmeet.pk})
        self.assertTrue(Favorite.objects.filter(fav_user=self.user1).exists())
    
    def test_unfavorite_database(self):
        '''
        お気に入りを解除したらデータベースから削除される
        '''
        Favorite.objects.create(fav_user=self.user1, tmeet=self.tmeet)
        self.client.post(reverse('tmitter:favorite'), data={'pk': self.tmeet.pk})
        self.assertFalse(Favorite.objects.filter(fav_user=self.user1).exists())


class TmeetFavDetailViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.tmeet = Tmeet.objects.create(author=self.user1, content='This is a tmeet for favorite test.')
        Favorite.objects.create(fav_user=self.user1, tmeet=self.tmeet)
        self.client.login(username="username1", password='password_a')

    def test_fav_user_list(self):
        '''
        tmeet_fav_detailにアクセスすると、
        そのツミートをお気に入りにしたアカウントが表示される
        '''
        response = self.client.get(reverse('tmitter:tmeet_fav_detail', args=str(self.tmeet.pk)))
        for fav_user_name in Favorite.objects.values('fav_user__username').all():
            self.assertContains(response, fav_user_name["fav_user__username"])


class AccountFavDetailViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("username1", "", "password_a")
        self.tmeet = Tmeet.objects.create(author=self.user1, content='This is a tmeet for favorite test.')
        Favorite.objects.create(fav_user=self.user1, tmeet=self.tmeet)
        self.client.login(username="username1", password='password_a')

    def test_fav_user_list(self):
        '''
        tmeet_fav_detailにアクセスすると、
        そのアカウントがお気に入りにしたツミートが表示される
        '''
        response = self.client.get(reverse('tmitter:account_fav_detail', args=str(self.user1.id)))
        for tmeet in Favorite.objects.values('tmeet__content').all():
            self.assertContains(response, tmeet["tmeet__content"])
