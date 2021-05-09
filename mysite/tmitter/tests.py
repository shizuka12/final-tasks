from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Tmeet
from django.urls import reverse

# Create your tests here.

data1 = {
    'username': 'username1',
    'password': 'password_1'
}
data2 = {
    'username': 'username2',
    'password': 'password_2'
}

class TopViewTests(TestCase):
    def setUp(self):
        self.timeline_list = []
        for i in range(1,3):
            data = 'data{}'.format(str(i))
            user = User.objects.create_user(data)
            self.client.login(data=data)
            content = 'This is a timeline test by username' + str(i)
            Tmeet.objects.create(author_id=i, content=content)
            self.timeline_list.append(content)
    
    def test_of_timeline(self):
        '''
        トップページにアクセスしたら、
        すべてのユーザーのツミートが表示される
        '''
        self.client.login(data=data2)
        print(reverse('tmitter:top', args=str(2)))
        response = self.client.get(reverse('tmitter:top', args=str(2)))
        queryset = response.context['tmeet_list']
        for i in range(2):
            self.assertEqual(queryset[i].content, self.timeline_list[i])
