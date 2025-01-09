from django.urls import path, include

urlpatterns = [
    path('posts/', include('python_blog.urls'))
]
