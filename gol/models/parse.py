from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from gol.models.task import Task


class Parse(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    input_text = models.TextField(default='')
    params = models.TextField(default='')
    state = models.TextField(default='')
    report = models.TextField(default='')
    evaluation_time = models.DecimalField(max_digits=8, decimal_places=3,
                                          default=0)
    datetime = models.DateTimeField(default=timezone.now)
    parsed = models.TextField(default='')
