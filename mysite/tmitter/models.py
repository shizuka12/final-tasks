from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tmeet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    tmeeted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.follower} follows {self.following}"
