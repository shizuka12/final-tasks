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

class Favorite(models.Model):
    fav_user = models.ForeignKey(User, related_name='faved_tmeet', on_delete=models.CASCADE)
    tmeet = models.ForeignKey(Tmeet, related_name='faved_user', on_delete=models.CASCADE)
    fav_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fav_user.username + " favorited " + self.tmeet.content
