from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, PasswordInput
from django.contrib.auth.models import User


class LoginForm(Form):
    username = CharField(label="Username:", max_length=30)
    password = CharField(label="Password:", widget=PasswordInput())


class CustomizeAccountForm(PasswordChangeForm):
    username = CharField(label="Username:", max_length=30)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(user, *args, **kwargs)

    def clean_username(self):
        newusername = self.cleaned_data['username']
        if newusername == self.user.username:
            return newusername

        if User.objects.filter(username=newusername).exists():
            raise ValidationError("Username already exists!", code="user_already_exists")

        return newusername

    def save(self, commit=True):
        super(PasswordChangeForm, self).save(commit)
        self.user.username = self.cleaned_data.get("username")
        self.user.save()
