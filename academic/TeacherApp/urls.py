from django.conf.urls import url

from . import views

app_name = "TeacherApp"
urlpatterns = [
    url(r'^$', views.teacher_main, name='main'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/(?P<course_id>\d+)/$', views.students, name='students'),
    url(r'^courses/(?P<course_id>\d+)/(?P<student_id>\d+)/$', views.edit, name='edit')

]
