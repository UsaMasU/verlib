from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout')
]
