from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test.utils import setup_test_environment

from LoginApp.models import Client, Staff, Student, Teacher, StudyLine


class TestUtils:
    def create_student(self):
        st = StudyLine.INFO
        s = Student(first_name="Test1", last_name="test1", email="bla@bla.com", id_number=10,study_line=st)
        s.save()
        return s

    def create_staff(self):
        c = Staff(first_name="aest1", last_name="test1", email="bla@bla.com")
        c.save()
        return c

    def create_teacher(self):
        s = Teacher(first_name="test1", last_name="test1", email="bla@bla.com")
        s.save()
        return s

class ViewTests(TestCase):
    def test_access(self):
        c = self.client
        response = c.get("/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/')
        response = c.get("/student/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/student/')
        response = c.get("/teacher/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/teacher/')
        response = c.get("/login/")
        self.assertEquals(response.status_code, 200)
        response = c.get("/teacher/courses/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/logout/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/change-account/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/reset-pass/")
        self.assertEquals(response.status_code, 200)

    def test_reset(self):
        stud = TestUtils().create_student()
        crtPass = stud.get_temp_pass()
        stud.is_activated = True
        stud.save()

        response = self.client.post("/reset-pass/", {"username": stud.user.username, "email": stud.email})
        self.assertEquals(response.status_code, 200)
        stud.refresh_from_db()
        self.assertFalse(stud.is_activated)
        self.assertNotEqual(stud.get_temp_pass(), crtPass)
        stud.delete()

    def test_login(self):
        stud = TestUtils().create_student()
        response = self.client.post("/login/", {"username" : stud.user.username, "password":stud.get_temp_pass()})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/")
        response = self.client.get("/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/student/")
        response = self.client.get("/student/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/change-account/")

        chpass = {"username" : "myuser123", "old_password": stud.get_temp_pass(), "new_password1": "parola123parola",
                  "new_password2": "parola123parola"}
        response = self.client.post("/change-account/", chpass)
        self.assertEquals(response.status_code, 200)
        stud.refresh_from_db()
        stud.user.refresh_from_db()
        self.assertEquals(stud.user.username, "myuser123")
        self.assertTrue(stud.is_activated)

        response = self.client.get("/student/")
        self.assertEquals(response.status_code, 200)
        stud.delete()

class StudentMethodTests(TestCase):
    def test_user(self):
        s = TestUtils().create_student()
        self.assertEquals(s.get_user(), "tete10")
        self.assertEquals(s.study_line, StudyLine.INFO)

    def test_duplicate(self):
        tu = TestUtils()
        tu.create_student()
        try:
            tu.create_student()
            self.assertFalse(True)
        except IntegrityError:
            self.assertTrue(True)


class TeacherMethodTests(TestCase):
    def test_user(self):
        s = TestUtils().create_teacher()
        self.assertEquals(s.get_user(), "ttest1")
        self.assertEquals(s.type, "teacher")

    def test_duplicate(self):
        tu = TestUtils()
        tu.create_teacher()
        try:
            tu.create_teacher()
            self.assertFalse(False)
        except IntegrityError:
            self.assertTrue(False)


class ClientStaffMethodTests(TestCase):
    def test_reset_pass(self):
        c = TestUtils().create_staff()
        temp_pass = c.get_temp_pass()
        c.is_activated = True
        c.save()
        c.reset_password()
        self.assertFalse(c.is_activated)
        self.assertNotEqual(temp_pass, c.get_temp_pass())

    def test_delete(self):
        c = TestUtils().create_staff()
        self.assertEquals(User.objects.count(), 1)
        c.delete()
        self.assertEquals(User.objects.count(), 0)

    def test_get_temp(self):
        c = TestUtils().create_staff()
        c.is_activated = True
        self.assertEquals(c.get_temp_pass(), "")

    def test_pass_len(self):
        c = Client(first_name="test1", last_name="test1", email="bla@bla.com")
        self.assertEquals(len(c._gen_pass()), 13)

    def test_user_name(self):
        c = TestUtils().create_staff()
        self.assertEquals(c.user.username, "atest1")

    def test_user_duplicate(self):
        c = TestUtils().create_staff()
        c2 = TestUtils().create_staff()
        self.assertEquals(c2.user.username, "atest10")
        c3 = TestUtils().create_staff()
        self.assertEquals(c3.user.username, "atest11")

    def test_type(self):
        c = TestUtils().create_staff()
        self.assertEquals(c.user.groups.first().name, "staff")
        self.assertEquals(c.type, "staff")

    def test_type2(self):
        c = TestUtils().create_staff()
        c._set_type("masa")
        self.assertEquals(c.user.groups.count(), 2)
        self.assertEquals(c.type, "masa")

    def test_active(self):
        c = TestUtils().create_staff()
        self.assertEquals(c.is_activated, False)
