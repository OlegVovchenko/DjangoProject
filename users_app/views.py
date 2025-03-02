from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegisterForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    next_page = 'main'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
        return form

def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('main')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('main')

def profile_user(request):
    pass