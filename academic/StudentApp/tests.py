from django.test import TestCase


# Create your tests here.
class ViewTests(TestCase):
    def test_access(self):
        c = self.client
        response = c.get("/student/grades/")
        self.assertEquals(response.status_code, 302)
