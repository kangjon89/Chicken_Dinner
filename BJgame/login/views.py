from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt


def index(request):
    return render(request, 'login.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['name'] = request.POST['name']
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        a = User.objects.create(
            name=request.POST['name'], email=request.POST['email'], password=pw_hash, money=100)

        request.session['user_id'] = a.id
        request.session['user_name'] = request.POST['name']
        request.session['user_money'] = a.money
        return redirect('/lobby')


def login(request):
    errors = User.objects.login_error(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        u = User.objects.get(email=request.POST['email_login'])
        request.session['user_name'] = u.name
        request.session['user_id'] = u.id
        request.session['user_money'] = u.money
        return redirect('/lobby')


def logout(request):
    request.session.flush()
    return redirect('/')
