from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  # 添加这行导入

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
    if request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 验证用户
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 登录成功，重定向到主界面
            login(request, user)
            return redirect('main_page')
        else:
            # 登录失败，显示错误信息
            return render(request, 'tasks/登录.html', {'error_message': '用户名或密码不正确'})
    
    # GET请求，显示登录表单
    return render(request, 'tasks/登录.html')

def chat_assistant(request):
    return render(request, 'tasks/聊天助手.html')
