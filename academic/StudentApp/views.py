from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.


@login_required(login_url=reverse_lazy('LoginApp:login'))
def main_page(request):
    return render(request, "StudentApp/student_main.html", {"has_permission" : True})