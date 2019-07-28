"""May_T URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import blog.views
import accounts.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',blog.views.index,name='index'),
    path('read/<int:post_id>',blog.views.read,name='read'),
    path('create/',blog.views.create,name='create'),
    path('update/<int:post_id>',blog.views.update,name='update'),
    path('delete/<int:post_id>',blog.views.delete,name='delete'),
    path('search/',blog.views.search,name='search'),
    path('category/',blog.views.category,name='category'),
    path('c_create/<int:post_id>',blog.views.c_create,name='c_create'),
    path('c_delete/<int:comment_id>',blog.views.c_delete,name='c_delete'),
    path('login/',accounts.views.login,name='login'),
    path('signup/',accounts.views.signup,name='signup'),
    path('logout/',accounts.views.logout,name='logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
