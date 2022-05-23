from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser

MAX_LENGTH_FOR_TASK_NAME = 100


class Task(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_FOR_TASK_NAME,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
    )
    tasks_author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
        related_name='tasks_author',
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Executor'),
        related_name='tasks_executor',
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_('Labels'),
        related_name='tasks',
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey(
        Label,
        on_delete=models.PROTECT,
    )
