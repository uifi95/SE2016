from django.conf.urls import url, include

from . import views

app_name = "TeacherApp"
urlpatterns = [
    url(r'^$', views.teacher_main, name='main'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/(?P<course_id>\d+)/$', views.students, name='students'),
    url(r'^courses/(?P<course_id>\d+)/(?P<student_id>\d+)/$', views.edit, name='edit'),
    url(r'^optionals/$', views.optionals, name='optionals'),
    url(r'^optionals/add/$', views.add_optional, name='add_opt'),
    url(r'^optionals/delete/(?P<optional_id>\d+)/$', views.delete_optional, name='delete_optional'),

]
