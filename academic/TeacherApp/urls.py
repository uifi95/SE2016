from django.conf.urls import url, include

from . import views

app_name = "TeacherApp"
urlpatterns = [
    url(r'^$', views.teacher_main, name='main'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/(?P<course_id>\d+)&(?P<group_number>\d+)&(?P<period>\d+)/$', views.students, name='students'),
    url(r'^courses/(?P<course_id>\d+)&(?P<group_number>\d+)&(?P<period>\d+)/(?P<student_id>\d+)/$', views.edit,
        name='edit'),
    url(r'^optionals/$', views.optionals, name='optionals'),
    url(r'^optionals/add/$', views.add_optional, name='add_opt'),
    url(r'^view_packages/$', views.view_all_packages, name='view_all_packages'),
    url(r'^optionals/delete/(?P<optional_id>\d+)/$', views.delete_optional, name='delete_optional'),
    url(r'^dchief/$', views.dchief_page, name='dchief_page'),
    url(r'^dchief/add/$', views.create_package, name='package_create'),
    url(r'^dchief/view/$', views.view_packages, name='view_packages'),
    url(r'^dchief/delete/(?P<package_id>\d+)/$', views.delete_package, name='delete_package'),
    url(r'^dchief/viewcourses/$', views.view_all_courses, name='view_all_courses'),
    url(r'^dchief/statistics/$', views.statistics, name='statistics'),
]
