from django.conf.urls import url

from . import views

app_name = "TeacherApp"
urlpatterns = [
    url(r'^$', views.teacher_main, name='main'),
    url(r'^grades/', views.grades, name='grades')

]
