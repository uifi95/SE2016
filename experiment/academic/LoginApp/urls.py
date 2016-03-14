from django.conf.urls import url

from . import views

app_name= "LoginApp"
urlpatterns = [
    url(r'^$', views.main_page, name='main'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^change-pass/',views.activate_account, name='change_account')
]