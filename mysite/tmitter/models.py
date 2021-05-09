from django.conf import settings
from django.db import models

# Create your models here.
class Tmeet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    tmeeted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
