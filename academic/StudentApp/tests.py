from django.test import TestCase

# Create your tests here.
from StudentApp.models import StudyLine


class StudyLineTest(TestCase):
    def testFields(self):
        s = StudyLine(name="info")
        self.assertEquals(s.name, "info")
