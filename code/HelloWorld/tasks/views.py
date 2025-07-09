from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task
from .forms import TaskForm

def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    # 获取当前时间
    now = timezone.now()
    
    # 任务筛选逻辑
    pending_tasks = Task.objects.filter(is_completed=False, deadline__gte=now)
    overdue_tasks = Task.objects.filter(is_completed=False, deadline__lt=now).order_by('deadline')
    completed_tasks = Task.objects.filter(is_completed=True).order_by('-completed_at')
    
    # 新增：计算逾期任务的生命损失时间（拖延时间的1/10）
    total_lost_life_seconds = 0
    for task in overdue_tasks:
        delay = now - task.deadline
        total_lost_life_seconds += delay.total_seconds() / 10  # 拖延时间的1/10
    
    # 转换为小时（保留1位小数）
    lost_life_hours = round(total_lost_life_seconds / 3600, 1)
    
    priority_counts = {
        'high': pending_tasks.filter(priority=3).count(),
        'medium': pending_tasks.filter(priority=2).count(),
        'low': pending_tasks.filter(priority=1).count()
    }
    
    return render(request, 'task_list.html', {
        'form': form, 
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completed_tasks': completed_tasks,
        'priority_counts': priority_counts,
        'lost_life_hours': lost_life_hours  # 传递生命损失数据
    })

# 添加删除任务视图
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return redirect('task_list')

# 新增：完成任务视图
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
    return redirect('task_list')
