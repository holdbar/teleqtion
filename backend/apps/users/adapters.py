from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Constructs the email confirmation (activation) url.
        """
        current_site = request.build_absolute_uri('/')
        url = reverse(
            "confirm_account",
            args=[emailconfirmation.key])
        return current_site + url
