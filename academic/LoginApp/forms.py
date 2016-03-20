from django.contrib.auth import authenticate
from django.forms import Form, CharField, PasswordInput, ValidationError


class LoginForm(Form):
    username = CharField(label="Username:", max_length=30)
    password = CharField(label="Password:", widget=PasswordInput())

