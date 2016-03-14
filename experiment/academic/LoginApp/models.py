from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# TODO: add django validators for name min length
class Student(models.Model):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    id_number = models.IntegerField("Identification number")
    email = models.EmailField()
    user = models.ForeignKey(User)
    temp_pass = models.CharField(max_length=40)
    is_activated = models.BooleanField("Active", default=False)

    def _gen_user(self):
        return "abcdefg"

    def _gen_pass(self):
        return "1234abcd"

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
        self.temp_pass = self._gen_pass()

        self.user = User.objects.create_user(username=self._gen_user(), password=self.temp_pass, email=self.email)
        super(Student, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        user = self.user
        self.user = None
        self.save()
        user.delete()
        super(Student, self).delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.last_name + " " + self.first_name
