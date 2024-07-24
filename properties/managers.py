import logging
from datetime import timedelta

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class FutureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(for_date__gte=timezone.now())

    def upcoming(self, start=None, end=None):
        end = end or (timezone.localdate() + timedelta(days=14))

        qs = self.get_queryset()
        qs = qs.filter(for_date__gte=start) if start else qs
        return qs.filter(for_date__lte=end)

    def __repr__(self):
        return "Occurrence Future Manager 🔮"
