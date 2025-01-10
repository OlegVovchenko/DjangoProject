from django.contrib import admin
from django.urls import path, include
from python_blog.views import main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('posts/', include('python_blog.urls')),
]
