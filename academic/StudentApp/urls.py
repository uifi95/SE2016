from django.conf.urls import url

from . import views

app_name = "StudentApp"
urlpatterns = [
    url(r'^$', views.main_page, name='main'),
    url(r'^grades/', views.grades, name='grades')

]
