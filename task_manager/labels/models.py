from django.db import models
from django.utils.translation import gettext_lazy as _

MAX_LENGTH_FOR_LABEL_NAME = 50


class Label(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_FOR_LABEL_NAME,
        null=False,
        unique=True,
        verbose_name=_('Name'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
