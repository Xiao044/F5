from django.db import models
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, '低'),
        (2, '中'),
        (3, '高'),
    ]
    name = models.CharField(max_length=200, verbose_name='任务名称')
    deadline = models.DateTimeField(verbose_name='截止日期')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name='重要级')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['deadline']
        verbose_name = '任务'
        verbose_name_plural = '任务'

# Create your models here.
