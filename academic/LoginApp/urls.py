from django.conf.urls import url

from . import views

app_name = "LoginApp"
urlpatterns = [
    url(r'^$', views.main_page, name='main'),
    url(r'^login/', views.login_page, name='login'),
    url(r'^logout/', views.logout_page, name='logout'),
    url(r'^change-account/', views.change_account, name='change_account')
]
