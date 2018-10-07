from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('blog/', posts_list, name='main_url'),
    path('post/<str:slug>', PostDetail.as_view(), name='post_detail_url'),
    path('search/', search_que, name='search_que'),
    path('mods/', mods_view, name='mods_url'),
    path('register/', Registration.as_view(), name='reg_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('logout/', session_del, name='session_del_url')
]
