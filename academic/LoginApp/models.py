from __future__ import unicode_literals
import string
import struct
from os import urandom
from random import shuffle

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

# Create your models here.


class Client(models.Model):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    email = models.EmailField()
    user = models.ForeignKey(User, null=True)
    temp_pass = models.CharField(max_length=40)
    is_activated = models.BooleanField("Active", default=False)
    type = models.CharField(max_length=30)

    def _gen_user(self):
        u_name = (self.first_name[0] + self.last_name).lower()
        base = u_name
        count = 0
        while User.objects.filter(username=u_name).all().count():
            u_name = base + str(count)
            count += 1
        return u_name

    def _set_type(self, type):
        group, created = Group.objects.get_or_create(name=type)
        self.user.groups.add(group)
        self.type = type

    @staticmethod
    def _gen_pass():
        alphabet = list(string.ascii_letters + string.digits + "!@#$%^&*")
        shuffle(alphabet)
        rbytes = urandom(13)
        password = ""
        for el in rbytes:
            bval = struct.unpack('B', bytes([el]))[0]
            password += alphabet[bval % len(alphabet)]
        return password

    def _create_user(self):
        self.temp_pass = self._gen_pass()
        self.user = User.objects.create_user(username=self._gen_user(), password=self.temp_pass, email=self.email)


    def get_temp_pass(self):
        if self.is_activated:
            return ""
        else:
            return self.temp_pass

    def get_user(self):
        return self.user.get_username()

    get_user.short_description = "Username"
    get_temp_pass.short_description = "Temporary password"

    def __str__(self):
        return self.last_name + " " + self.first_name

class Staff(Client):
    class Meta:
        verbose_name_plural = 'Staff'

    def save(self, *args, **kwargs):
        if not self.pk:
            self._create_user()
            self._set_type("staff")
            self.user.is_staff = True
            self.user.save()
            self.user.is_admin = True
            self.user.save()
            self.user.is_superuser = True
            self.user.save()
        super(Staff, self).save(*args, **kwargs)

class Student(Client):
    id_number = models.IntegerField("Identification number", unique=True)

    def _gen_user(self):
        if len(self.last_name) >= 2:
            firstTwo = self.last_name[:2]
        else:
            firstTwo = self.last_name
        if len(self.first_name) >= 2:
            lastTwo = self.first_name[:2]
        else:
            lastTwo = self.first_name
        return (firstTwo + lastTwo + str(self.id_number)).lower()

    def save(self, *args, **kwargs):
        if not self.pk:
            self._create_user()
            self._set_type("student")
        super(Student, self).save(*args, **kwargs)



# SIGNALS start here
# Global flag to avoid infinite recursion
is_in_pre_delete = False
@receiver(pre_delete, sender=Client)
def pre_delete_client(sender, **kwargs):
    global is_in_pre_delete
    if is_in_pre_delete:
        return
    if not isinstance(kwargs["instance"], Client):
        return
    is_in_pre_delete = True
    user = kwargs["instance"].user
    kwargs["instance"].user = None
    user.delete()
    is_in_pre_delete = False
