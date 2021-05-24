from django.urls import path
from .views import signup, signin, signout, follow, unfollow, following_detail, follower_detail

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('follow/<int:user_id>/', follow, name='follow'),
    path('unfollow/<int:user_id>/', unfollow, name='unfollow'),
    path('following_detail/<int:user_id>/', following_detail, name='following_detail'),
    path('follower_detail/<int:user_id>/', follower_detail, name='follower_detail'),
]
