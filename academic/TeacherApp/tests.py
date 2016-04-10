from django.test import TestCase


# Create your tests here.
class ViewTests(TestCase):
    def test_access(self):
        c = self.client
        response = c.get("/teacher/courses/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/teacher/optionals/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/teacher/courses/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/teacher/optionals/add/")
        self.assertEquals(response.status_code, 302)
        response = c.get("/teacher/optionals/delete/")
        self.assertEquals(response.status_code, 404)
