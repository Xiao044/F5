from django.db import models
from django.contrib.auth.models import User

# 扩展用户模型，存储排行榜所需的额外信息
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    total_score = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)
    last_ranking_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

# Create your models here.

# 任务分类模型
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 任务模型
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', '待完成'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('expired', '已过期'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(default=1)
    score = models.IntegerField(default=10)  # 完成任务获得的积分
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['created_by']),
            models.Index(fields=['assigned_to']),
        ]


# 排行榜模型
class Ranking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_ranking')
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}"
