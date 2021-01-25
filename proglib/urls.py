from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='lib_main'),
    path('lib/<str:slug>', CategoryItem.as_view(), name='lib_category'),
    path('lib/plc/<str:slug>', ItemDetail.as_view(), name='lib_plc'),
    path('lib/hmi/<str:slug>', ItemDetail.as_view(), name='lib_hmi'),
    path('lib/tag/<str:slug>', ItemDetail.as_view(), name='lib_tag'),
    path('lib/item/<str:slug>', ItemDetail.as_view(), name='lib_item')
]
