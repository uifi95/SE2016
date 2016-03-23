from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from LoginApp.user_checks import student_check


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(student_check, login_url=reverse_lazy('LoginApp:login'))
def main_page(request):
    return render(request, "StudentApp/student_main.html", {"has_permission" : True})