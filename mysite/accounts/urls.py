from django.urls import path
from .views import signup, signin, top

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('top/', top, name='top'),
]
