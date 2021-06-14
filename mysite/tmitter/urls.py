from django.urls import path
from .views import top, accountpage, tmeet, tmeet_detail, delete_tmeet, favorite, tmeet_fav_detail, account_fav_detail

app_name = 'tmitter'
urlpatterns = [
    path('top/', top, name='top'),
    path('accountpage/<int:user_id>/', accountpage, name='accountpage'),
    path('tmeet/', tmeet, name='tmeet'),
    path('tmeet_detail/<int:pk>/', tmeet_detail, name='tmeet_detail'),
    path('delete_tmeet/<int:pk>/', delete_tmeet, name='delete_tmeet'),
    path('favorite/', favorite, name='favorite'),
    path('tmeet_fav_detail/<int:pk>/', tmeet_fav_detail, name='tmeet_fav_detail'),
    path('account_fav_detail/<int:user_id>/', account_fav_detail, name='account_fav_detail'),
]
