from django.urls import path
from .views import top, accountpage, tmeet, tmeet_detail, delete_tmeet

app_name = 'tmitter'
urlpatterns = [
    path('top/<int:user_id>/', top, name='top'),
    path('accountpage/<int:user_id>/', accountpage, name='accountpage'),
    path('tmeet/<int:user_id>/', tmeet, name='tmeet'),
    path('tmeet_detail/<int:user_id>/<int:pk>/', tmeet_detail, name='tmeet_detail'),
    path('delete_tmeet/<int:user_id>/<int:pk>/', delete_tmeet, name='delete_tmeet'),
]
