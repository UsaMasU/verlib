"""verlib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from proglib.views import Search, search

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    #path('search/', search, name='lib_search'),
    path('comment/', include('comment.urls')),
    path('account/', include('users.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('prog/', include('proglib.urls')),
    path('search/', Search.as_view(), name='search'),
    path('', include('proglib.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
