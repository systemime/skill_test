import logging

from django.db.models import signals
from django.dispatch import receiver

from .models import Country

logger = logging.getLogger(__name__)

from django.db.models.signals import post_save, pre_save  # noqa


@receiver(signals.pre_save, sender=Country)
def before_dispatch_info_change(
    sender, instance: Country, **kwargs
):  # pylint: disable=all

    instance.is_remove = True
    print(kwargs)
    logger.error(kwargs)


# pre_save.connect(before_dispatch_info_change, sender=Country)


@receiver(signals.post_save, sender=Country)
def after_dispatch_info_change(
    sender, instance: Country, **kwargs
):  # pylint: disable=all
    print(kwargs)
    logger.error(kwargs)


# post_save.connect(after_dispatch_info_change, sender=Country)
