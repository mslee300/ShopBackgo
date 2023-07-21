from django.contrib import admin
from django.urls import path, include
from . import views, upsize_views

urlpatterns = [
    path('', views.index, name='index'),
    path('promoupdate/', views.index, name='index'),
    path('upsize/', upsize_views.index, name='index'),
    path('screenshot/', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
]
