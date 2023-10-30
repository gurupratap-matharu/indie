import logging

from django.conf import settings
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)


def post_save_receiver(sender, instance, created, **kwargs):
    """
    Placeholder method to execute logic when a custom user is saved or updated.
    """

    # Just logging for now to check functionality
    logger.info(
        "Hey Veer you just saved/updated a CustomUser!\n \
        I am the post_save hook that got triggered"
    )
    logger.info("sender %s" % sender)
    logger.info("instance %s" % instance)
    logger.info("created %s" % created)
    logger.info("kwargs %s" % kwargs)

    # Your stuff here


# Wire up our callback with active AUTH USER MODEL
post_save.connect(
    post_save_receiver,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="post_save_receiver",
)
