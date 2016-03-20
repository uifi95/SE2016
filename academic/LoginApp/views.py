from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import admin

# Create your views here.
from LoginApp.forms import LoginForm
from django.forms import ValidationError

def main_page(request):
    if not request.user.is_authenticated():
        return redirect('LoginApp:login')

    if request.user.is_staff:
        return redirect('admin:index')


def login_page(request):
    if request.user.is_authenticated():
        return redirect('LoginApp:main')
    if request.method != 'POST':
        newForm = LoginForm()
        return render(request, "LoginApp/login.html", {'form':newForm})
    authForm = LoginForm(data=request.POST)
    if authForm.is_valid():
        username = authForm.cleaned_data["username"]
        password = authForm.cleaned_data["password"]
        user = authenticate(username=username, password = password)
        if not user:
            authForm.add_error(None, ValidationError("User or password wrong!"))
            return render(request, "LoginApp/login.html", {'form': authForm})

        login(request, user)
        return redirect("LoginApp:main")
    else:
         return render(request, "LoginApp/login.html", {'form': authForm})
