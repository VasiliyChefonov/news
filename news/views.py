from django.shortcuts import render, redirect
from news.models import *
import hashlib
import datetime
import random
import string


def remove_cookie():
    response = redirect("/login")
    response.set_cookie("user_token", "", max_age=0)
    return response


def log_out(request):
    response = remove_cookie()
    return response


def check_auth(request):
    user_token = get_token(request)
    if user_token != -1:
        try:
            person = Person.objects.get(token=user_token)
            return person.admin_level
        except Person.DoesNotExist:
            return -1
    else:
        return -1


def get_token(request):
    if 'user_token' in request.COOKIES:
        token = request.COOKIES.get('user_token')
        return token
    else:
        return -1


def generate_token():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(30))


def set_cookie(auth, form_login):
    if auth == 1:
        response = redirect("/admin")
    else:
        response = redirect("/")
    login_person = Person.objects.get(login=form_login)
    login_person.token = generate_token()
    login_person.save()
    response.set_cookie("user_token", login_person.token)
    return response


def authorize(form_login, password):
    try:
        login_person = Person.objects.get(login=form_login)
        if login_person.password != password:
            return -1
        else:
            return login_person.admin_level
    except Person.DoesNotExist:
        return -1


def hash_password(password):
    hash_pass = hashlib.sha3_256(password).hexdigest()
    return hash_pass


def login(request):
    if request.POST:
        user_login = request.POST.get("login")
        password = request.POST.get("password")
        password = password.encode('utf-8')
        hash_pass = hash_password(password)
        auth = authorize(user_login, hash_pass)
        if auth == -1:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль!'})
        else:
            response = set_cookie(auth, user_login)
            return response
    else:
        return render(request, 'login.html')


def main(request):
    auth_status = check_auth(request)
    if auth_status != -1:
        articles = Article.objects.all()
        return render(request, 'index.html', {"articles": articles, "admin_lvl": auth_status})
    else:
        return redirect("/login")


def admin(request):
    if request.POST:
        form_title = request.POST.get("title")
        form_content = request.POST.get("content")
        article = Article(title=form_title, content=form_content, date=datetime.datetime.now())
        article.save()
        return redirect("/")
    else:
        auth_status = check_auth(request)
        if auth_status == 1:
            return render(request, 'admin.html')
        else:
            return redirect("/")


