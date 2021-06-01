from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + " follows " + self.following.username
