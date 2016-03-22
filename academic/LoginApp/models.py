from __future__ import unicode_literals
import string
import struct
from os import urandom
from random import shuffle

from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.

# TODO: add django validators for name min length
class Student(models.Model):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    id_number = models.IntegerField("Identification number", unique=True)
    email = models.EmailField()
    user = models.ForeignKey(User, null=True)
    temp_pass = models.CharField(max_length=40)
    is_activated = models.BooleanField("Active", default=False)

    def _gen_user(self):
        if len(self.last_name) >= 2:
            firstTwo = self.last_name[:2]
        else:
            firstTwo = self.last_name
        if len(self.first_name) >= 2:
            lastTwo = self.first_name[:2]
        else:
            lastTwo = self.first_name
        return firstTwo + lastTwo + str(self.id_number)

    def _gen_pass(self):
        alphabet = list(string.ascii_letters + string.digits + "!@#$%^&*")
        shuffle(alphabet)
        bytes = urandom(13)
        password = ""
        for el in bytes:
            bval = struct.unpack('B', el)[0]
            password += alphabet[bval % len(alphabet)]
        return password

    def get_temp_pass(self):
        if self.is_activated:
            return ""
        else:
            return self.temp_pass

    def get_user(self):
        return self.user.get_username()

    get_user.short_description = "Username"
    get_temp_pass.short_description = "Temporary password"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.temp_pass = self._gen_pass()

            self.user = User.objects.create_user(username=self._gen_user(), password=self.temp_pass, email=self.email)

            group, created = Group.objects.get_or_create(name='student')
            self.user.groups.add(group)
        super(Student, self).save(*args, **kwargs)

    # Don't work on bulk, will have to use signals
    def delete(self, *args, **kwargs):
        user = self.user
        user.delete()
        super(Student, self).delete(*args, **kwargs)

    def __str__(self):
        return self.last_name + " " + self.first_name
