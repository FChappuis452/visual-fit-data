from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class RedirectAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/fitness"
        return path