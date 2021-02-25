from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .forms import UserRegisterForm, UserLoginForm, ContactForm


def user_logout(request):
    logout(request)
    return redirect('lib_main')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='ProgTeam')
            user.groups.add(group)
            user.is_staff = True
            user.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('lib_main')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lib_main')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {"form": form})


def user_feedback(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'proglib@vertek.ru', ['vsemenov@vertek.ru'], fail_silently=False)
            mail = True
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('user_feedback')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'users/email.html', {"form": form})
