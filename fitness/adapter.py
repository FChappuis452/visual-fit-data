from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class RedirectAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/steps"
        return path

    def get_logout_redirect_url(self, request):
        path = "/"
        return path