from django.core.urlresolvers import reverse


def basics_processors(request):
    return {'site_title': "Academic Authentication System", 'main_url': reverse("LoginApp:main")}