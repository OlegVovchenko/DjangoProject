from django.urls import path
from users_app.views import login_user, CustomLogoutView, register_user, profile_user

app_name = 'users'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_user, name='register'),
    path('profile/', profile_user, name='profile'),
]

 