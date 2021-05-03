from django.urls import path
from .views import signup, signin, signout

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
]
