from django.shortcuts import render

# Create your views here.

def main_page(request):
    return render(request, 'tasks/主界面.html')

def task_square(request):
    return render(request, 'tasks/任务广场.html')

def team_collaboration(request):
    return render(request, 'tasks/团队协作.html')

def study_partner(request):
    return render(request, 'tasks/学习搭档.html')

def ranking(request):
    return render(request, 'tasks/排行榜.html')

def data_statistics(request):
    return render(request, 'tasks/数据统计.html')

def add_task(request):
    return render(request, 'tasks/添加任务.html')

def login(request):
    return render(request, 'tasks/登录.html')

def chat_assistant(request):
    return render(request, 'tasks/聊天助手.html')
