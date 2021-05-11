from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Tmeet
from django.urls import reverse
import time

# Create your tests here.
class TopViewTests(TestCase):
    def setUp(self):
        self.timeline_list = []
        self.user = User.objects.create_user('username1', '', 'password_1')
        self.client = Client()
        self.client.login(username='username1', password='password_1')
        content = 'This is a timeline test by username1'
        Tmeet.objects.create(author_id=1, content=content)
        self.timeline_list.append(content)
        self.user = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        content = 'This is a timeline test by username2'
        Tmeet.objects.create(author_id=2, content=content)
        self.timeline_list.append(content)
        self.timeline_list.reverse()
    
    def test_of_timeline(self):
        '''
        トップページにアクセスしたら、
        すべてのユーザーのツミートが新しい順に表示される
        '''
        response = self.client.get(reverse('tmitter:top', args=str(2)))
        queryset = response.context['tmeet_list']
        for i in range(2):
            self.assertEqual(queryset[i].content, self.timeline_list[i])


class AccountpageViewTests(TestCase):
    def setUp(self):
        self.accountpage_list = []
        self.user = User.objects.create_user('username1', '', 'password_1')
        self.client = Client()
        self.client.login(username='username1', password='password_1')
        for i in range(2):
            content = 'This is a accountpage test' +str(i+1)+ ' by username1'
            Tmeet.objects.create(author_id=1, content=content)
            time.sleep(0.1)
        self.user = User.objects.create_user('username2', '', 'password_2')
        self.client.login(username='username2', password='password_2')
        for i in range(2):
            content = 'This is a accountpage test' +str(i+1)+ ' by username2'
            Tmeet.objects.create(author_id=2, content=content)
            self.accountpage_list.append(content)
            time.sleep(0.1)
        self.accountpage_list.reverse()

    def test_of_tmeetlist(self):
        '''
        アカウントページにアクセスしたら、
        そのユーザーのツミートが新しい順に表示される
        '''
        response = self.client.get(reverse('tmitter:accountpage', args=str(2)))
        queryset = response.context['tmeet_list']
        for i in range(2):
            self.assertEqual(queryset[i].content, self.accountpage_list[i])
