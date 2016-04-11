from django.conf.urls import url
from django.core.urlresolvers import reverse, resolve


def basics_processors(request):
    student_pages = [reverse('StudentApp:main'), reverse('StudentApp:grades')]
    if request.path in student_pages:
        return {'site_title': "Academic Students", 'main_url': reverse("StudentApp:main")}
    return {'site_title': "Academic Authentication System",
            "is_chief": request.user.groups.filter(name="dchief").exists(), 'main_url': reverse("LoginApp:main")}
