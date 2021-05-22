
from django.urls import path
from .views import top, accountpage, tmeet, tmeet_detail, delete_tmeet

app_name = 'tmitter'
urlpatterns = [
    path('top/', top, name='top'),
    path('accountpage/<int:user_id>/', accountpage, name='accountpage'),
    path('tmeet/', tmeet, name='tmeet'),
    path('tmeet_detail/<int:pk>/', tmeet_detail, name='tmeet_detail'),
    path('delete_tmeet/<int:pk>/', delete_tmeet, name='delete_tmeet'),
]
