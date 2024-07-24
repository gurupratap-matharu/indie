import logging

from django.conf import settings
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)


def post_save_receiver(sender, instance, created, **kwargs):
    """
    Placeholder method to execute logic when a custom user is saved or updated.
    """

    # Your stuff here
    logger.info(
        "sender:%s instance:%s created:%s kwargs:%s "
        % (sender, instance, created, kwargs)
    )


# Wire up our callback with active AUTH USER MODEL
post_save.connect(
    post_save_receiver,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="post_save_receiver",
)
