# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import os


def main_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")

    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))

    return HttpResponse("Welcome to home page")


def activate_account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('LoginApp:login'))

    chpage = os.path.join("LoginApp", "chpass.html")
    # TODO: Check user is actually student
    stud = request.user.student_set.first()
    user =request.user
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        new_pass = request.POST['new_password']
        retype = request.POST['retype_password']
        if not user.check_password(password):
            return render(request, chpage, {'username':request.user.username, 'state': "Wrong current password!"})
        if new_pass != retype:
            return render(request, chpage, {'username':request.user.username, 'state': "New password must match retype!"})
        user.username = username
        user.set_password(new_pass)
        stud.is_activated = True
        user.save()
        stud.save()
        return HttpResponse("Welcome to home page") #TODO
    else:
        return render(request, chpage, {'username':request.user.username})

def login_user(request):
    auth_page = os.path.join("LoginApp", "auth.html")
    state = "Please log in below..."
    if request.user.is_authenticated():
        return HttpResponse("You are already authenticated!")
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect(reverse('admin:index'))
                else:
                    # Assume student, just for proof of concept
                    stud = user.student_set.first()
                    if stud.is_activated:
                        return HttpResponse("Welcome to home page")
                    else:
                        return HttpResponseRedirect(reverse('LoginApp:change_account'))
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

        return render(request, auth_page, {'state':state, 'username': username})
    else:
        context = {'state':state}
        return render(request, auth_page, context)