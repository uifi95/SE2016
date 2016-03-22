from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, "StudentApp/student_main.html", {"has_permission" : True})