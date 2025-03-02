from django.urls import path
from users_app.views import CustomLoginView, logout_user, RegisterView, profile_user

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_user, name='profile'),
]

 