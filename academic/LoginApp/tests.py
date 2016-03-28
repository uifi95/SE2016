from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from LoginApp.models import Client, Staff, Student, Teacher


# Create your tests here.
from StudentApp.models import StudyLine


# class StudentMethodTests(TestCase):
#     def test_user(self):
#         st = StudyLine(name="info")
#         s = Student(first_name="Test1", last_name="test1", email="bla@bla.com", id_number=10,study_line=st)
#         s.save()
#         self.assertEquals(s.get_user(), "tete10")
#         self.assertEquals(s.study_line, "info")
#     def test_duplicate(self):
#         st = StudyLine(name="info")
#         s = Student(first_name="test1", last_name="test1", email="bla@bla.com", id_number=10,study_line=st)
#         s.save()
#         s2 = Student(first_name="test1", last_name="test1", email="bla@bla.com", id_number=10,study_line=st)
#         try:
#             s2.save()
#             self.assertFalse(True)
#         except IntegrityError:
#             self.assertTrue(True)


class TeacherMethodTests(TestCase):
    def test_user(self):
        s = Teacher(first_name="Test1", last_name="test1", email="bla@bla.com", id_number=10)
        s.save()
        self.assertEquals(s.get_user(), "tete10")
        self.assertEquals(s.type, "teacher")

    def test_duplicate(self):
        s = Teacher(first_name="test1", last_name="test1", email="bla@bla.com", id_number=10)
        s.save()
        s2 = Teacher(first_name="test1", last_name="test1", email="bla@bla.com", id_number=10)
        try:
            s2.save()
            self.assertFalse(True)
        except IntegrityError:
            self.assertTrue(True)


class ClientStaffMethodTests(TestCase):
    def test_delete(self):
        c = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c.save()
        self.assertEquals(User.objects.count(), 1)
        c.delete()
        self.assertEquals(User.objects.count(), 0)

    def test_get_temp(self):
        c = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c.save()
        c.is_activated = True
        self.assertEquals(c.get_temp_pass(), "")

    def test_pass_len(self):
        c = Client(first_name="test1", last_name="test1", email="bla@bla.com")
        self.assertEquals(len(c._gen_pass()), 13)

    def test_user_name(self):
        c = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c.save()
        self.assertEquals(c.user.username, "atest1")

    def test_user_duplicate(self):
        c = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c.save()
        c2 = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c2.save()
        self.assertEquals(c2.user.username, "atest10")
        c3 = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c3.save()
        self.assertEquals(c3.user.username, "atest11")

    def test_type(self):
        c = Staff(first_name="test1", last_name="test1", email="bla@bla.com")
        c.save()
        self.assertEquals(c.user.groups.first().name, "staff")
        self.assertEquals(c.type, "staff")

    def test_type2(self):
        c = Staff(first_name="test1", last_name="test1", email="bla@bla.com")
        c.save()
        c._set_type("masa")
        self.assertEquals(c.user.groups.count(), 2)
        self.assertEquals(c.type, "masa")

    def test_active(self):
        c = Staff(first_name="test1", last_name="test1", email="bla@bla.com")
        c.save()
        self.assertEquals(c.is_activated, False)
