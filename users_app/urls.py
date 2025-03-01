from django.urls import path
from users_app.views import CustomLoginView, logout_user, register_user, profile_user

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('profile/', profile_user, name='profile'),
]

 