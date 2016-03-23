from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import admin

# Create your views here.
from LoginApp.forms import LoginForm, CustomizeAccountForm
from django.forms import ValidationError

@login_required(login_url=reverse_lazy('LoginApp:login'))
def main_page(request):
    if request.user.is_staff:
        return redirect('admin:index')

    if request.user.groups.filter(name="student").count():
        return redirect('StudentApp:main')


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
        if not request.GET["next"]:
            return redirect("LoginApp:main")
        else:
            return HttpResponseRedirect(request.GET["next"])
    else:
         return render(request, "LoginApp/login.html", {'form': authForm})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def logout_page(request):
    logout(request)
    return render(request, "LoginApp/logout.html", {"title" : "Logged out!"})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def change_account(request):
    if request.method != 'POST':
        newForm = CustomizeAccountForm(user=request.user)
        newForm.fields["username"].initial = request.user.username;
        return render(request, "LoginApp/change_account.html", {'form':newForm})

    form = CustomizeAccountForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        if form.user.student_set.count() and not form.user.student_set.first().is_activated:
            # Maybe change with a parent model for all types of entities?
            obj = form.user.student_set.first()
            obj.is_activated = True
            obj.save()
        return render(request, "LoginApp/done_change_account.html", {'title': "Account updated!"})
    else:
        return render(request, "LoginApp/change_account.html", {'form':form})
