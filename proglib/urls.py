from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='lib_main'),
    path('lib/<str:slug>', CategoryView.as_view(), name='lib_category'),
    path('lib/author/<str:slug>', ItemAuthorView.as_view(), name='lib_author'),
    path('lib/plc/<str:slug>', PLCView.as_view(), name='lib_plc'),
    path('lib/hmi/<str:slug>', HMIView.as_view(), name='lib_hmi'),
    path('lib/tag/<str:slug>', TagView.as_view(), name='lib_tag'),
    path('lib/item/<str:slug>', ItemView.as_view(), name='lib_item')
]
