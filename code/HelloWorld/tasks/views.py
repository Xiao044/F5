from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from datetime import datetime

# 计算变化率的辅助函数
def calculate_percentage_change(current_count, last_count):
    if last_count > 0:
        return ((current_count - last_count) / last_count) * 100
    return 0

# 任务列表视图：展示任务创建表单和任务列表
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

    # 获取本周的任务数量
    current_total_tasks = Task.objects.filter(is_completed=False, deadline__gte=now).count() + Task.objects.filter(is_completed=True).count()
    current_in_progress_tasks = Task.objects.filter(is_completed=False, deadline__gte=now, deadline__lt=now + timezone.timedelta(weeks=1)).count()
    current_completed_tasks = Task.objects.filter(is_completed=True, completed_at__gte=now).count()
    current_overdue_tasks = Task.objects.filter(is_completed=False, deadline__lt=now).count()

    # 获取上周的任务数量
    last_week_start = now - timezone.timedelta(weeks=1)
    last_week_end = now

    last_total_tasks = Task.objects.filter(is_completed=False, deadline__gte=last_week_start, deadline__lt=last_week_end).count() + Task.objects.filter(is_completed=True, completed_at__gte=last_week_start, completed_at__lt=last_week_end).count()
    last_in_progress_tasks = Task.objects.filter(is_completed=False, deadline__gte=last_week_start, deadline__lt=last_week_end).count()
    last_completed_tasks = Task.objects.filter(is_completed=True, completed_at__gte=last_week_start, completed_at__lt=last_week_end).count()
    last_overdue_tasks = Task.objects.filter(is_completed=False, deadline__lt=last_week_end).count()

    # 计算变化百分比
    total_tasks_change_percentage = calculate_percentage_change(current_total_tasks, last_total_tasks)
    in_progress_tasks_change_percentage = calculate_percentage_change(current_in_progress_tasks, last_in_progress_tasks)
    completed_tasks_change_percentage = calculate_percentage_change(current_completed_tasks, last_completed_tasks)
    overdue_tasks_change_percentage = calculate_percentage_change(current_overdue_tasks, last_overdue_tasks)

    # 获取高、中、低优先级任务的数量
    pending_tasks = Task.objects.filter(is_completed=False, deadline__gte=now)
    overdue_tasks = Task.objects.filter(is_completed=False, deadline__lt=now).order_by('deadline')
    completed_tasks = Task.objects.filter(is_completed=True).order_by('-completed_at')

    # 计算逾期任务的生命损失时间（拖延时间的1/10）
    total_lost_life_seconds = 0
    for task in overdue_tasks:
        delay = now - task.deadline
        total_lost_life_seconds += delay.total_seconds() / 10  # 拖延时间的1/10
    
    # 转换为小时（保留1位小数）
    lost_life_hours = round(total_lost_life_seconds / 3600, 1)

    # 获取高、中、低优先级任务的数量
    high_count = pending_tasks.filter(priority=3).count()
    medium_count = pending_tasks.filter(priority=2).count()
    low_count = pending_tasks.filter(priority=1).count()

    # 计算任务的总数量
    total_tasks = pending_tasks.count() + overdue_tasks.count() + completed_tasks.count()

    # 计算每个优先级任务的比例
    high_priority_ratio = (high_count / total_tasks) * 100 if total_tasks else 0
    medium_priority_ratio = (medium_count / total_tasks) * 100 if total_tasks else 0
    low_priority_ratio = (low_count / total_tasks) * 100 if total_tasks else 0

    # 任务优先级分配建议
    high_priority_advice = f"高优先级任务占 {high_priority_ratio:.2f}%，这些任务通常最紧急且最重要，建议优先处理。"
    medium_priority_advice = f"中优先级任务占 {medium_priority_ratio:.2f}%，这些任务可以在完成高优先级任务后进行处理。"
    low_priority_advice = f"低优先级任务占 {low_priority_ratio:.2f}%，这些任务可以在空闲时间或高优先级任务完成后处理。"

    # 优先级计数
    priority_counts = {
        'high': high_count,
        'medium': medium_count,
        'low': low_count
    }

    # 计算任务的变化文本
    def get_change_text(change_percentage):
        if change_percentage > 0:
            return f"比上周增长 {change_percentage:.2f}%"
        elif change_percentage < 0:
            return f"比上周减少 {abs(change_percentage):.2f}%"
        else:
            return "与上周持平"

    return render(request, 'task_list.html', {
        'form': form,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completed_tasks': completed_tasks,
        'priority_counts': priority_counts,
        'lost_life_hours': lost_life_hours,  # 传递生命损失数据
        'high_priority_advice': high_priority_advice,
        'medium_priority_advice': medium_priority_advice,
        'low_priority_advice': low_priority_advice,
        'total_tasks': total_tasks,
        'total_tasks_change_text': get_change_text(total_tasks_change_percentage),
        'in_progress_tasks_change_text': get_change_text(in_progress_tasks_change_percentage),
        'completed_tasks_change_text': get_change_text(completed_tasks_change_percentage),
        'overdue_tasks_change_text': get_change_text(overdue_tasks_change_percentage),
    })

# 添加任务视图：显示任务添加表单并处理提交
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

# 删除任务视图：删除指定的任务
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return redirect('task_list')

# 完成任务视图：将任务标记为已完成
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
    return redirect('task_list')

# 任务详情视图：展示任务详情页面（待办、逾期、已完成）
def task_detail(request):
    # 获取当前时间
    now = timezone.now()

    # 任务筛选逻辑
    pending_tasks = Task.objects.filter(is_completed=False, deadline__gte=now)
    overdue_tasks = Task.objects.filter(is_completed=False, deadline__lt=now).order_by('deadline')
    completed_tasks = Task.objects.filter(is_completed=True).order_by('-completed_at')

    # 确保 deadline 为 datetime 类型（如果它是字符串类型）
    for task in pending_tasks:
        if isinstance(task.deadline, str):
            task.deadline = timezone.make_aware(datetime.strptime(task.deadline, '%Y-%m-%d %H:%M'))

    for task in overdue_tasks:
        if isinstance(task.deadline, str):
            task.deadline = timezone.make_aware(datetime.strptime(task.deadline, '%Y-%m-%d %H:%M'))

    for task in completed_tasks:
        if isinstance(task.deadline, str):
            task.deadline = timezone.make_aware(datetime.strptime(task.deadline, '%Y-%m-%d %H:%M'))

    return render(request, 'task_detail.html', {
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completed_tasks': completed_tasks,
    })
