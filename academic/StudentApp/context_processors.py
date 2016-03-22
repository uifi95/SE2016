from django.core.urlresolvers import reverse


def basics_processors(request):
    return {'site_title': "Academic Students", 'main_url': reverse("StudentApp:main")}