import logging

from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter

logger = logging.getLogger(__name__)


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):  # noqa
        # user = request.user
        # company = user.companies.first()
        # url = company.get_admin_url() if company else settings.LOGIN_REDIRECT_URL
        url = settings.LOGIN_REDIRECT_URL
        logger.info("redirecting user to {url}", extra={"url": url})

        return url
